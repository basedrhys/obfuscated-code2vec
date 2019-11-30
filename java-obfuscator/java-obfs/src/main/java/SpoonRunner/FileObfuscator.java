package SpoonRunner;

import org.apache.commons.io.FileUtils;
import spoon.Launcher;
import spoon.SpoonException;
import spoon.reflect.code.CtLocalVariable;
import spoon.reflect.declaration.*;
import spoon.support.compiler.VirtualFile;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class FileObfuscator implements Runnable {

    public void run() {
        obfuscate();
    }

    private static String thousandFormatString = "%d/%d - Obfuscated, taken %f seconds\n";
    private static String fileAlteredString = "\t %d - file already altered: %s\n";


    private String m_newPath, m_oldPath;

    HashMap<String, Integer> classHM = new HashMap<>();
    HashMap<String, Integer> methodParamHM = new HashMap<>();
    HashMap<String, Integer> methodLocalHM = new HashMap<>();

    public FileObfuscator(String newPath, String oldPath) {
        m_newPath = newPath;
        m_oldPath = oldPath;
    }

    private void obfuscateToFile() {
        int count = SpoonRunner.fileCounter.incrementAndGet();
        File newFile = new File(m_newPath);

        if (!newFile.exists()) {
            // Create the obfuscated version of the class
            String fileString = "", newClass = "";
            try {
                fileString = readInFile(m_oldPath);
                newClass = obfuscateFile(fileString);
            } catch (Exception e) {
                e.printStackTrace();
            }

            if (!newClass.equals("")) {
                // Write it to our new file
                try (PrintWriter out = new PrintWriter(newFile, "UTF-8")) {
                    out.print(newClass);
                } catch (Exception e) {
                    System.err.print(m_oldPath + " - ");
                    e.printStackTrace();
                }

                if (count % 1000 == 0) {
                    System.out.printf(thousandFormatString, count, SpoonRunner.listLength,
                            (System.nanoTime() - SpoonRunner.time0) / 1e9);
                }
            }
        } else {
            System.out.printf(fileAlteredString, count, m_newPath);
        }
    }

    private String readInFile(String path) {
        StringBuilder sb = new StringBuilder();

        try {
            InputStream is = new FileInputStream(path);
            BufferedReader buf = new BufferedReader(new InputStreamReader(is));

            String line = buf.readLine();

            while (line != null) {
                sb.append(line).append("\n");
                line = buf.readLine();
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        return sb.toString();
    }

    private void obfuscate() {
        if (SpoonRunner.mode == SpoonRunner.Mode.FOLDER) {
            obfuscateToFile();
        } else {
            processFileMethods();
        }
    }

    private void processFileMethods() {
        String fileString = readInFile(m_oldPath);

        Collection<CtType<?>> allTypes = returnAllTypes(fileString);
        List<Object> allFunc = new ArrayList<>();

        for (CtType classOrInterface : allTypes) {
            try {
                CtClass newClass = (CtClass<?>) classOrInterface;
                CtClass obfuscated = obfuscateToCtClass(newClass);

                allFunc.addAll(obfuscated.getMethods());
            } catch (ClassCastException e) {
//                System.err.println("\tCouldn't cast to class, might be interface");
            }
        }

        String result = allFunc.stream().map(a -> a.toString()).collect(Collectors.joining("\n_METHOD_SPLIT_\n"));

        System.out.println(result);
    }

    private String obfuscateToString(CtClass newClass) {
        CtClass res = _obfuscateCtClass(newClass);
        if (res != null) {
            return res.toString();
        } else {
            return "";
        }
    }

    private CtClass obfuscateToCtClass(CtClass newClass) {
        return _obfuscateCtClass(newClass);
    }


    private CtClass _obfuscateCtClass(CtClass newClass) {
        try {
            classHM.clear();

            // First refactor the variables within the methods
            for (Object ctMethod : newClass.getMethods()) {
                methodParamHM.clear();
                methodLocalHM.clear();

                CtMethod method = (CtMethod) ctMethod;

                // Refactor the method parameters first
                method.getElements(a -> a.getClass() == spoon.support.reflect.declaration.CtParameterImpl.class)
                        .forEach(a -> {
                            CtParameter param = (CtParameter) a;
                            renameVar(param, "param");
                        });

                // Now refactor the method local variables
                method.getElements(a -> a.getClass() == spoon.support.reflect.code.CtLocalVariableImpl.class)
                        .forEach(b -> {
                            CtLocalVariable localVariable = (CtLocalVariable) b;
                            renameVar(localVariable, "local");
                        });
            }

            // Refactor the fields
            newClass.getElements(a -> a.getClass() == spoon.support.reflect.declaration.CtFieldImpl.class)
                    .forEach(a -> {
                        CtField field = (CtField) a;
                        renameVar(field, "field");
                    });

            // Now refactor the constructors
            // Note that constructors are ignored for code2vec preprocessing so this step is somewhat unnecessary
            for (Object ctConstructor : newClass.getConstructors()) {
                methodParamHM.clear();
                methodLocalHM.clear();

                CtConstructor constructor = (CtConstructor) ctConstructor;

                // Refactor the constructor parameters first
                constructor.getElements(a -> a.getClass() == spoon.support.reflect.declaration.CtParameterImpl.class)
                        .forEach(a -> {
                            CtParameter param = (CtParameter) a;
                            renameVar(param, "param");
                        });

                // Now refactor the method local variables
                constructor.getElements(a -> a.getClass() == spoon.support.reflect.code.CtLocalVariableImpl.class)
                        .forEach(b -> {
                            CtLocalVariable localVariable = (CtLocalVariable) b;
                            renameVar(localVariable, "local");
                        });
            }

            return newClass;
        } catch (SpoonException e) {
            System.err.println("\tFile:\t" + m_oldPath + "\t" + e);
            return null;
        } catch (Exception e) {
            System.err.print(m_oldPath.toString() + " - ");
            e.printStackTrace();
            return null;
        }
    }

    private String obfuscateFile(String fileString) {
        Collection<CtType<?>> allTypes = returnAllTypes(fileString);
        StringBuilder sb = new StringBuilder();

        for (CtType classOrInterface : allTypes) {
            try {
                CtClass newClass = (CtClass<?>) classOrInterface;
                String obfuscated = obfuscateToString(newClass);
                if (!obfuscated.equals(""))
                    sb.append(obfuscated).append("\n\n");
            } catch (ClassCastException e) {
//                System.err.println("\tCouldn't cast to class, might be interface");
            }
        }

        return sb.toString().trim();
    }

    private Collection<CtType<?>> returnAllTypes(String code) {
        Launcher launcher = new Launcher();
        launcher.addInputResource(new VirtualFile(code));
        launcher.getEnvironment().setNoClasspath(true);
        launcher.getEnvironment().setAutoImports(true);
        Collection<CtType<?>> allTypes = launcher.buildModel().getAllTypes();

        return allTypes;
    }

    private void renameVar(CtVariable variable, String type) {
        if (variable == null || variable.getType() == null) {
            return;
        }
        String varClass = variable.getType().toString();
        // Strip off any new line characters
        varClass = varClass.replaceAll("[\r\n]", "");
        int varNum = 0;
        try {
            // Replace square brackets with the word Array
            if (varClass.matches(".*\\[\\].*")) {
                varClass = varClass.replace("[]", "Array");
            }

            // If there are any non word characters in the class (e.g. <, >, .)
            if (varClass.matches(".*[^\\w].*")) {
                String[] testSplit = varClass.split("[^\\w.]");
                for (int i = 0; i < testSplit.length; i++) {
                    // Get this word and remove any leading fullstops
                    String word = getClassAfterDots(testSplit[i]);
                    if (word.length() == 1) {
                        word = "";
                    }
                    testSplit[i] = word;
                }

                varClass = String.join("", testSplit);
            }

            if (type == "field") {
                varNum = getVarNum(classHM, varClass);
            } else if (type == "param") {
                varNum = getVarNum(methodParamHM, varClass);
            } else if (type == "local") {
                varNum = getVarNum(methodLocalHM, varClass);
            }
            String newName;
            if (SpoonRunner.randomObfs) {
                newName = randomVarName(10);
            } else {
                newName = String.format("%s_%s_%d", type, varClass, varNum);
            }
            changeVarNameTo(variable, newName);
        } catch (Exception e) {
            String newName = String.format("%s_%s_%d", type, "unk", varNum);
            changeVarNameTo(variable, newName);
            e.printStackTrace();
        }
    }

    private void changeVarNameTo(CtVariable<?> variable, String newName) {
        new CtRenameGenericVarRefactoring().setTarget(variable).setNewName(newName).refactor();
    }

    private int getVarNum(HashMap<String, Integer> hm, String type) {
        if (hm.containsKey(type)) {
            hm.put(type, hm.get(type) + 1); // Increment the counter for this var type
            return hm.get(type);    // Return the updated variable number
        } else {
            hm.put(type, 1);    // Create the first entry for this var
            return 1;
        }
    }

    private String getClassAfterDots(String classString) {
        if (classString.length() == 0) {
            return classString;
        }
        return classString.substring(classString.lastIndexOf(".") + 1, classString.length());
    }

    private static final String ALPHA_NUMERIC_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    public static String randomVarName(int count) {
        StringBuilder builder = new StringBuilder();
        while (count-- != 0) {
            int character = (int)(Math.random()*ALPHA_NUMERIC_STRING.length());
            builder.append(ALPHA_NUMERIC_STRING.charAt(character));
        }
        return builder.toString();
    }
}
