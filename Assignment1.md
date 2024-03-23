# COMPSCI 752

## Student ID: 437681250
## Name: Shuo Mao



# XML and XPath

## (a) For each node of the tree, write down the corresponding pre- and post-identifier

###  - pre-identifier is assigned as visit node in pro-order traversal (node-left-right)
from tree structure in fig.1 we can assign the pre-order traversal as : 

- doc -> a -> b -> a -> a ->b -> a -> b -> a -> a -> a -> b -> b

in the pre-identifier: doc(root) = 1 <br>
-> a(1st layer, 1st node, 1st 'a') = 2 <br>
->  b(2nd layer, 1st node, 1st 'b') = 3 <br>
-> a(3rd layer, 1st node, 2nd 'a') = 4 <br>
-> a(3rd layer, 2nd node, 3rd 'a') = 5<br>
-> b(2nd layer, 2nd node, 2nd 'b') = 6 <br>
-> a (3rd layer, 1 node, 4th 'a') = 7 <br>
-> b (2nd layer, 3rd node, 3rd 'b') = 8<br>
-> a (3rd layer, 1st node, 5th 'a') = 9<br>
-> a(3rd layer, 2nd node, 6th = 'a') = 10  <br>
-> a (3nd layer, 3rd node, 7th = 'a') = 11<br>
-> b(4th layer, 1st node, 4th 'b') = 12 <br>
-> b(4th layer, 2nd node, 5th 'b') = 13<br>

### - post-identifier is assigned as visit node in post-order traversal (right-left-node)

- a -> a -> b -> a -> b -> a -> a -> a -> b -> b -> b -> a -> doc

in post-identifier: 
a (3rd layer, 1st node, 2nd 'a') = 1<br>
-> a (3rd layer, 2nd node, 3rd 'a') = 2<br>
-> b (2nd layer, 1st node, 1st 'b') = 3<br>
-> a (3rd layer, 1st node, 4th 'a') = 4<br>
-> b (2nd layer, 2nd node, 2nd 'b') = 5<br>
-> a (3rd layer, 1st node, 4th 'a') = 6 <br>
-> a (3rd layer, 2nd node, 5th 'a') = 7 <br>
-> a (3rd layer, 3rd node, 6th 'a') = 8 <br>
-> b (4th layer, 1rd node, 4th 'b') = 9<br>
-> b (4th layer, 2nd node, 5th 'b') = 10 <br>
-> b (2nd layer, 3rd node, 3rd 'b') = 11<br>
-> a (1st layer, 1st node, 1st 'a') = 12<br>
-> doc (root)<br>


## (b) Write down the XML document that corresponds to this tree
the XML document that corresponds to this tree will be like : 
```xml
<doc>
    <a>
        <b>
            <a></a>
            <a></a>
         </b>

        <b>
            <a></a>
         </b>

        <b>
            <a></a>
            <a>
                <b></b>
         
                <b></b>
            </a>
            <a></a>
         </b>

    </a>
</doc>
```


### (c) With respect to the given context node, marked in pink, evaluate the following axes on the tree. List the pre-identifier of each node that each axis returns.

#### i. following::a
following::a will return all labled 'a' node in pre-identifier which means it will return all node with label 'a' of the pinked node
in graphic it will be like this : 
```
          doc
             |
             a
           / |     \
          b  b          b(current node)
         /|  |   /       |        \
        a a  a a(return) a(return) a (return)
                        / \
                       b   b
```
#### ii. ancestor-or-self::node()
ancestor-or-self::node will selects all ancestor nodes of the current node, including the node itself.In the graphic it will look like : 
```
            doc(return)
             |
             a(return)
           / | \
          b  b  b(current node)(return)
         /|  | /|\
        a a  a a a a
                 / \
                b   b
```

#### iii. preceding-sibling::b 
preceding-sibling::b will select all 'b' nodes that share same parent with current node, which means it will return all 'b' node that under same layers. In graphic it will look like: 

```
                        doc
                        |
                        a
           /            |       \
          b(return)  b(return)    b(current node)
         /|             |        /|\
        a a             a       a a a
                                 / \
                                b   b
```


### convert each of the following queries into the corresponding XPath expression, and evaluate it on the tree by listing the pre-identifier of the nodes returned.

#### i. For every element child m of some element node, and for every node n that is the third among all b-labelled element children of m, return the node that is the second among all element children for some descendant-or-self node of n.

This query asking for: 
- Element child 'm' of some element node
- A node 'n' taht is thrid among all 'b' labelled children from 'm' 
- return the node that is the second among all element children for some decendant-or-self node of 'n'

we can use '//*' to select all nodes from the tree, then filter by '[b[3]]' which means drop all node expect the nodse with 3rd 'b' label on it, finally '/*2' selects the second child element of each of nodes that is been filtered. 

So the XPath expressin will be :
```
 //*[b[3]]/*[2]
```

in graphic

```
            doc
             |
             a
           / | \
          b  b  b
         /|  | /  |        \
        a a  a a  a(return)  a
                 / \
                b   b

```


#### ii. Return every element node whose number of preceding siblings is the same as its number of following siblings.

To complete this task the count function are required, we need to count the current node's preceding siblings and following siblibngs. given XPath express: 
```
//*[count(preceding-sibling::*) = count(following-sibling::*)]
```



#### iii. Return every element node that is not a child. 

In order to return every element node that is a child, which mean it's asking for to return a root node, because only parent node doesn't require a parent node, therefor to return a node taht is not a child we can use XPath :
```
/* or /doc(if we know the lable of root node)
```

# XQuery


### (a) For every distinct location l for which no trek with rating less than 85 exists, return an element node with label location that has the following content: i) a child element labelled location name with the name of the location as text content, and  ii) for each trek in that location, an element child labelled trek with the name of the trek as text content.

```
let $walks := //walks
let $filter_location := 
    for $l in distinct-values($walks/trek/location)
    where every $trek in $walks/trek[location = $l] satisfies $trek/rating >= 85
    return $l

return
    for $loc in $filter_location
    let $treks := $walks/trek[location = $loc]
    return 
        <location>
            <location-name>{$loc}</location-name>
            {
                for $trek in $treks
                return
                    <trek name="{$trek/@name}">
                        <rating>{$trek/rating}</rating>
                        <location>{$trek/location}</location>
                        <difficulty>{$trek/difficulty}</difficulty>
                    </trek>
            }
        </location>

```

### For the longest treks among those with difficulty moderate, return an element node labelled trek with i) attribute child name that contains the name of the trek and  ii)an element child labelled rating that has the text of the rating of the trek as content.

```
let $walks := //walks
let $moderate-treks := $walks/trek[difficulty = 'moderate']
let $max-length := max(
  for $trek in $moderate-treks
  let $length := xs:decimal(substring-before($trek/length, 'km'))
  return $length
)

return 
  for $trek in $moderate-treks
  let $length := xs:decimal(substring-before($trek/length, 'km'))
  where $length = $max-length
  return 
   	concat('name:', $trek/@name, ', rating:', $trek/rating)
```

### For every distinct difficulty, return an element node difficulty with  i) an attribute child called value that lists the difficulty, ii) an element child trek for every trek withthat difficulty, and  iii) an element child avg length that contains the average length over all of these treks

```
let $walks := //walks
let $distinct-difficulties := distinct-values($walks/trek/difficulty)

return
  for $difficulty in $distinct-difficulties
  let $treks := $walks/trek[difficulty = $difficulty]
  let $avg-length := avg(
    for $trek in $treks
    let $length-numeric := xs:decimal(substring-before($trek/length, 'km'))
    return $length-numeric
  )
 return
 <difficulty value="{$difficulty}">
{
  for $trek in $treks
  return 
    <trek>
      <details>{
        concat('name: ', $trek/@name, ', difficulty: ', $difficulty, ', length: ', $trek/length)
      }</details>
      <rating>{'rating :',$trek/rating}</rating>
    </trek>
}
<avg-length>Average length: {$avg-length} km</avg-length>
</difficulty>
```