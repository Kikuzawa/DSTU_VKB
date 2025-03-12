

package practice_2.question_2;

import lombok.extern.slf4j.Slf4j;
import practice_2.core.AbstractTree;
import practice_2.core.Node;

import java.util.Collection;
import java.util.LinkedList;
import java.util.stream.Collectors;

@Slf4j
public class BalancedTree<T extends Comparable<T>> extends AbstractTree<T> {

    public BalancedTree(Collection<T> input) {
        super(input);
    }

    @Override
    @SuppressWarnings("unchecked")
    protected Node<T> buildTree(Collection<T> input) {
        var forest = input.stream().map(Node::new).collect(Collectors.toList());

        log.debug("Initial start for balanced tree = {}", forest);

        while (forest.size() > 1) {
            var newForest = new LinkedList<Node<T>>();
            for (int i = 0; i < forest.size(); i += 2) {
                var leftChild = forest.get(i);
                var rightChild = i + 1 < forest.size() ? forest.get(i + 1) : null;
                var value = (T) Character.valueOf('+');

                log.debug("left child = {}, right child = {}", leftChild, rightChild);

                newForest.add(new Node<>(value, leftChild, rightChild));
            }
            forest = newForest;
        }

        return forest.getFirst();
    }

}
