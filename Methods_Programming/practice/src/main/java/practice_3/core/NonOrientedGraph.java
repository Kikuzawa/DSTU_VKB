

package practice_3.core;

public class NonOrientedGraph<T extends Comparable<T>> extends AbstractUnweightedGraph<T> {

    public NonOrientedGraph() {
        super();
    }


    public void addEdge(T start, T end) {
        UnweightedNode<T> startNode = vertices.computeIfAbsent(start, UnweightedNode::new);
        UnweightedNode<T> endNode = vertices.computeIfAbsent(end, UnweightedNode::new);

        startNode.connect(endNode);
        endNode.connect(startNode);
    }
}

