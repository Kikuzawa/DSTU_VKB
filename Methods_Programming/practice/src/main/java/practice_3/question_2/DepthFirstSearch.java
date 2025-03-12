package practice_3.question_2;

import lombok.extern.slf4j.Slf4j;
import practice_3.core.AbstractUnweightedGraph;
import practice_3.core.UnweightedNode;

import java.util.*;

@Slf4j
public class DepthFirstSearch {

    public static <T extends Comparable<T>> List<T> execute(T startValue, AbstractUnweightedGraph<T> graph) {
        if (graph == null || graph.getVertex(startValue) == null) {
            throw new IllegalArgumentException("Graph is null or start vertex not found: " + startValue);
        }

        List<T> path = new ArrayList<>();
        Set<UnweightedNode<T>> visited = new HashSet<>();
        UnweightedNode<T> startNode = graph.getVertex(startValue);

        log.debug("Start node = {}", startNode);

        dfsRecursive(startNode, visited, path);

        return path;
    }


    private static <T extends Comparable<T>> void dfsRecursive(UnweightedNode<T> current, Set<UnweightedNode<T>> visited, List<T> path) {
        visited.add(current);
        path.add(current.getValue());

        log.debug("Current node = {}, path = {}", current, path);

        for (UnweightedNode<T> neighbor : current.getNeighbors()) {
            if (!visited.contains(neighbor)) {
                dfsRecursive(neighbor, visited, path);
            }
        }
    }
}
