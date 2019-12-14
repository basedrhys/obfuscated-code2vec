package SpoonRunner;

import org.apache.commons.cli.*;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class SpoonRunner {

    static List<String> fileList = new ArrayList<>();
    static int listLength;
    static String sourceFolder;
    static String targetFolder;
    public static long time0, time1;

    public static AtomicInteger fileCounter = new AtomicInteger();

    public static boolean obfuscating = false;
    public static boolean randomObfs = false;

    public enum Mode {FOLDER, FILE}

    public static Mode mode;

    public static void main (String[] args) {
        Options options = new Options();

        Option s = new Option("s", "source", true, "Source file/folder for java files");
        s.setRequired(true);
        options.addOption(s);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;

        try {
            cmd = parser.parse(options, args, true);
        } catch (Exception e) {
            System.err.println(e.getMessage());
            formatter.printHelp("java-tool", options);

            System.exit(1);
        }

        File srcFile = new File(cmd.getOptionValue("s"));

        if (srcFile.isDirectory()) {
            mode = Mode.FOLDER;
            Option t = new Option("t", "target", true, "target folder for obfuscated files");
            t.setRequired(true);
            options.addOption(t);

            Option pNum = new Option("pNum", "partition-num", true, "Current partition number");
            pNum.setRequired(true);
            options.addOption(pNum);

            Option pTotal = new Option("pTotal", "partitions-total", true, "Total number of partitions");
            pTotal.setRequired(true);
            options.addOption(pTotal);

            Option threads = new Option("threads", true, "Number of threads for execution");
            threads.setRequired(true);
            options.addOption(threads);

            Option random = new Option("r","random", false, "Set the obfuscation method to random letters");
            options.addOption(random);

            try {
                cmd = parser.parse(options, args);
            } catch (Exception e) {
                System.err.println(e.getMessage());
                formatter.printHelp("java-obfuscator", options);

                System.exit(1);
            }

            sourceFolder = cmd.getOptionValue("s");
            targetFolder = cmd.getOptionValue("t");

            int partitionNum = Integer.parseInt(cmd.getOptionValue("pNum"));
            int partitionsTotal = Integer.parseInt(cmd.getOptionValue("pTotal"));
            int numThreads = Integer.parseInt(cmd.getOptionValue("threads"));

            if (cmd.hasOption("random")) {
                randomObfs = true;
                obfuscating = true;
                System.out.println("Obfuscating using random letters...");
            } else {
                System.out.println("Obfuscating using variable types...");
            }

            processFolders(partitionNum, partitionsTotal, numThreads);
        } else {
            mode = Mode.FILE;

            Option random = new Option("r","random", false, "Set the obfuscation method to random letters");
            options.addOption(random);

            Option obfus = new Option("o", "obfuscate", false, "Obfuscate the method before returning it");
            options.addOption(obfus);

            try {
                cmd = parser.parse(options, args);
            } catch (Exception e) {
                System.err.println(e.getMessage());
                formatter.printHelp("java-obfuscator", options);

                System.exit(1);
            }

            String inputFile = cmd.getOptionValue("s");

            if (cmd.hasOption("o")) {
                obfuscating = true;
            }

            if (cmd.hasOption("r")) {
                randomObfs = true;
                obfuscating = true;
            }

            FileObfuscator obfuscator = new FileObfuscator("", inputFile);
            obfuscator.run();
        }
    }

    private static void processFolders(int partitionNum, int numPartitions, int numThreads) {
        try {
            System.out.println("Making file list...");
            createFileList(new File(sourceFolder));
            System.out.println("Sorting...");
            Collections.sort(fileList);
        } catch (Exception e) {
            System.err.println("COULDNT CREATE FILE LIST");
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("Finished.");

        int partitionSize = fileList.size() / numPartitions;

        int partitionStartI = (partitionNum - 1) * partitionSize;
        int partitionEndI = partitionNum * partitionSize;

        // If we're in the last partition, set the end to be the end of the file list
        // So we don't miss any files
        if (partitionNum == numPartitions) {
            partitionEndI = fileList.size();
        }

        System.out.printf("%d total files...", fileList.size());
        fileList = fileList.subList(partitionStartI, partitionEndI);
        System.out.println(String.format("Starting and ending from index %d - %d\n", partitionStartI, partitionEndI));

        time0 = System.nanoTime();

        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(numThreads);

        listLength = fileList.size();

        while (fileList.size() > 0) {
            FileObfuscator obfuscator = new FileObfuscator(targetFolder + fileList.get(0),
                    sourceFolder + fileList.get(0));
            executor.execute(obfuscator);

            fileList.remove(0);
        }
        executor.shutdown();
        try{
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        } catch (Exception e) {

        }

        long time1 = System.nanoTime();
        System.out.println("Processing files took " + (time1 - time0) / 1e9 + " seconds");
    }

    public static void createFileList(File dir) throws IOException {
        File[] subdirs = dir.listFiles();
        for (File subdir : subdirs) {
            // Create the filename in the new directory
            String newFileName = subdir.getPath().substring(sourceFolder.length(), subdir.getPath().length());
            if (subdir.isDirectory()) {
                File newDir = new File(targetFolder + newFileName);
                newDir.mkdir();
                createFileList(subdir);
            } else {
                fileList.add(newFileName);
            }
        }
    }
}
