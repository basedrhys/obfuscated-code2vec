package SpoonRunner;

import org.apache.commons.io.FileUtils;
import spoon.Launcher;
import spoon.SpoonException;
import spoon.reflect.code.CtLocalVariable;
import spoon.reflect.declaration.*;
import spoon.support.compiler.VirtualFile;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

import static SpoonRunner.FileObfuscator.randomVarName;

public class ClassPreprocessor {

    String m_fileName;


    HashMap<String, Integer> methodParamHM = new HashMap<>();
    HashMap<String, Integer> methodLocalHM = new HashMap<>();
    HashMap<String, Integer> classHM = new HashMap<>();

    public ClassPreprocessor(String fileName) {
        m_fileName = fileName;
    }

    public void process() {
        StringBuilder sb = new StringBuilder();

        try {
            InputStream is = new FileInputStream(m_fileName);
            BufferedReader buf = new BufferedReader(new InputStreamReader(is));

            String line = buf.readLine();

            while (line != null) {
                sb.append(line).append("\n");
                line = buf.readLine();
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        String fileString = sb.toString();

        Collection<CtType<?>> allTypes = returnAllTypes(fileString);
        List<Object> allFunc = new ArrayList<>();

        for (CtType classOrInterface : allTypes) {
            try {
                CtClass newClass = (CtClass<?>) classOrInterface;
                CtClass obfuscated = obfuscateClass(newClass);

                allFunc.addAll(obfuscated.getMethods());
            } catch (ClassCastException e) {
//                System.err.println("\tCouldn't cast to class, might be interface");
            }
        }

        String result = allFunc.stream().map(a -> a.toString()).collect(Collectors.joining("\n_METHOD_SPLIT_\n"));

        System.out.println(result);
    }

    private Collection<CtType<?>> returnAllTypes(String code) {
        Launcher launcher = new Launcher();
        launcher.addInputResource(new VirtualFile(code));
        launcher.getEnvironment().setNoClasspath(true);
        launcher.getEnvironment().setAutoImports(true);
        Collection<CtType<?>> allTypes = launcher.buildModel().getAllTypes();

        return allTypes;
    }

    private CtClass obfuscateClass(CtClass newClass) {
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
            System.err.println("\t" + e);
            return null;
        }  catch (Exception e) {
            e.printStackTrace();
            return null;
        }
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

    public static void changeVarNameTo(CtVariable<?> variable, String newName) {
        if (SpoonRunner.obfuscating) {
            new CtRenameGenericVarRefactoring().setTarget(variable).setNewName(newName).refactor();
        } else {
            new CtRenameGenericVarRefactoring().setTarget(variable).setNewName(variable.getSimpleName()).refactor();
        }
    }

    private static int getVarNum(HashMap<String, Integer> hm, String type) {
        if (hm.containsKey(type)) {
            hm.put(type, hm.get(type) + 1); // Increment the counter for this var type
            return hm.get(type);    // Return the updated variable number
        } else {
            hm.put(type, 1);    // Create the first entry for this var
            return 1;
        }
    }

    private static String getClassAfterDots(String classString) {
        if (classString.length() == 0) {
            return classString;
        }
        return classString.substring(classString.lastIndexOf(".") + 1, classString.length());
    }
}
