package com.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws Exception {
        PluginManager pluginManager = new PluginManager();

        // Load the SamplePlugin1 from the plugin-sample1.jar file
        pluginManager.loadPlugin("plugin-sample1/build/libs/plugin-sample1.jar", "com.example.SamplePlugin");

        // Start the SamplePlugin1
        pluginManager.startPlugin("com.example.SamplePlugin");

        // Wait for user input
        Scanner scanner = new Scanner(System.in);
        System.out.print("Press enter to replace the plugin...");

        // Wait for user input before replacing the plugin
        scanner.nextLine();

        // Replace the SamplePlugin1 with the SamplePlugin2 from the plugin-sample2.jar file
        pluginManager.replacePlugin("plugin-sample2/build/libs/plugin-sample2.jar", "com.example.SamplePlugin");

        // Start the SamplePlugin2
        pluginManager.startPlugin("com.example.SamplePlugin");

        // Wait for user input
        System.out.print("Press enter key to exit...");
        scanner.nextLine();

        // Unload the SamplePlugin2
        pluginManager.unloadPlugin("com.example.SamplePlugin");
    }
}
