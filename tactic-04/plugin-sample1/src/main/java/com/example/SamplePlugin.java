package com.example;

public class SamplePlugin implements IPlugin {
    @Override
    public void start() {
        System.out.println("Starting SamplePlugin1...");
    }

    @Override
    public void stop() {
        System.out.println("Stopping SamplePlugin1...");
    }
}
