package org.example.laboratory__3.utils;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;

public class ParallelProcessor {
    private static final int NUM_THREADS = Runtime.getRuntime().availableProcessors();

    public static <T, R> List<R> processParallel(List<T> items, Function<T, R> processor) {
        ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);
        List<Future<R>> futures = new ArrayList<>();

        for (T item : items) {
            futures.add(executor.submit(() -> processor.apply(item)));
        }

        List<R> results = new ArrayList<>(items.size());
        for (Future<R> future : futures) {
            try {
                results.add(future.get());
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }

        executor.shutdown();
        return results;
    }

    public static <T, R> List<R> processParallelWithProgress(List<T> items, Function<T, R> processor, 
            Function<Integer, Void> progressCallback) {
        ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);
        List<Future<R>> futures = new ArrayList<>();
        CountDownLatch latch = new CountDownLatch(items.size());
        AtomicInteger completed = new AtomicInteger(0);

        for (T item : items) {
            futures.add(executor.submit(() -> {
                R result = processor.apply(item);
                completed.incrementAndGet();
                progressCallback.apply(completed.get());
                latch.countDown();
                return result;
            }));
        }

        List<R> results = new ArrayList<>(items.size());
        for (Future<R> future : futures) {
            try {
                results.add(future.get());
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }

        executor.shutdown();
        return results;
    }
} 