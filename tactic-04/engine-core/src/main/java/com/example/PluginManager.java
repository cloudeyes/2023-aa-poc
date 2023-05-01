package com.example;

import java.io.File;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class PluginManager {
  private Map<String, IPlugin> engines = new HashMap<>();

  public void loadPlugin(String jarFilePath, String pluginClassName) throws Exception {
    URL jarFileUrl = new File(jarFilePath).toURI().toURL();
    URLClassLoader classLoader = new URLClassLoader(new URL[] { jarFileUrl });
    Class<?> pluginClass = classLoader.loadClass(pluginClassName);
    IPlugin engine = (IPlugin) pluginClass.newInstance();
    engines.put(pluginClassName, engine);
    System.out.println("Plugin loaded successfully: " + pluginClassName);
  }

  public void unloadPlugin(String pluginClassName) {
    IPlugin engine = engines.remove(pluginClassName);
    if (engine != null) {
      engine.stop();
      System.out.println("Plugin unloaded successfully: " + pluginClassName);
    } else {
      System.out.println("Plugin not found: " + pluginClassName);
    }
  }

  public void replacePlugin(String jarFilePath, String pluginClassName) throws Exception {
    unloadPlugin(pluginClassName);
    loadPlugin(jarFilePath, pluginClassName);
  }

  public void startPlugin(String pluginClassName) {
    IPlugin engine = engines.get(pluginClassName);
    if (engine != null) {
        engine.start();
    } else {
        System.out.println("Plugin not found: " + pluginClassName);
    }
  }
}