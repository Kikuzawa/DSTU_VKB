package practice_2.question_1;

import lombok.extern.slf4j.Slf4j;
import practice_2.core.AbstractTree;
import practice_2.core.Node;

import java.util.Collection;
import java.util.LinkedList;
import java.util.stream.Collectors;

@Slf4j
public class Tree<T extends Comparable<T>> extends AbstractTree<T> {

    public Tree(Collection<T> input) {
        super(input);
    }
    @Override
    @SuppressWarnings("unchecked")
    protected Node<T> buildTree(Collection<T> input) {
        var forest = input.stream().map(Node::new).collect(Collectors.toList());

        var newForest = new LinkedList<Node<T>>();

        while (!forest.isEmpty()) {

            log.debug("initial collection = {}, forest = {}", input, forest);

            var leftChild = newForest.isEmpty() ? forest.removeFirst() : newForest.removeFirst();

            log.debug(
                    "Left Child = {}, initial collection = {}, forest = {}, forest is empty = {}",
                    leftChild,
                    forest,
                    newForest,
                    newForest.isEmpty()
            );

            var rightChild = forest.removeFirst();

            log.debug(
                    "Right Child = {}, initial collection = {}, forest = {}",
                    rightChild,
                    forest,
                    newForest
            );

            var value = (T) Character.valueOf('+');
            newForest.add(new Node<>(value, leftChild, rightChild));

            log.debug("Updated forest = {}", newForest);

        }

        return newForest.getFirst();
    }
}


