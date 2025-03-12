

package practice_3.core;


public class OrientedGraph<T extends Comparable<T>> extends AbstractUnweightedGraph<T> {

    public OrientedGraph() {
        super();
    }


    @Override
    public void addEdge(T start, T end) {
        UnweightedNode<T> startNode = vertices.computeIfAbsent(start, UnweightedNode::new);
        UnweightedNode<T> endNode = vertices.computeIfAbsent(end, UnweightedNode::new);
        startNode.connect(endNode);
    }



}
