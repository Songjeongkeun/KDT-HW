# B-Tree(Balanced-Tree)

B-Tree 는 트리 자료구조의 일종으로 이진트리를 확장해 하나의 노드가 가질 수 있는 자식 노드의 최대 숫자가 2보다 큰 트리 구조이다.

### 특징

1. 노드에는 2개 이상의 데이터(key)가 들어갈 수 있으며, 항상 정렬된 상태로 저장된다.

![image-20260604121056980](/Users/songjeong-geun/Library/Application Support/typora-user-images/image-20260604121056980.png)

2. 내부 노드는 ceil(M/2) ~ M 개의 자식을 가질 수 있다. 최대 M개의 자식을 가질 수 있는 B-Tree를 M 차 B-Tree라고 한다.

![image-20260604121150615](/Users/songjeong-geun/Library/Application Support/typora-user-images/image-20260604121150615.png)

>ceil() 함수는 올림 함수를 뜻한다. 즉 3차 B-Tree 의 leaf node 와 root node 를 제외한 내부 노드는 2~3개의 자식을 가질 수 있다.

3. 특정 노드의 데이터(key) 가 K개 라면 ,자식 노드의 개수는 K+1개여야 한다.

![image-20260604121422646](/Users/songjeong-geun/Library/Application Support/typora-user-images/image-20260604121422646.png)

4. 특정 노드의 왼쪽 서브 트리는 특정 노드의 key 보다 작은 값들로, 오른쪽 서브 트리는 큰 값들로 구성된다.

![image-20260604121514814](/Users/songjeong-geun/Library/Application Support/typora-user-images/image-20260604121514814.png)

5. 노드 내에 데이터는 ceil(M/2) - 1 개부터 최대 M-1 개 까지 포함될 수 있다.

   ![image-20260604121656257](/Users/songjeong-geun/Library/Application Support/typora-user-images/image-20260604121656257.png)

6. 모든 리프 노드들이 같은 레벨에 존재한다.

![image-20260604121739720](/Users/songjeong-geun/Library/Application Support/typora-user-images/image-20260604121739720.png)

- 모든 leaf node 들은 같은 레벨에 존재해야 한다. 즉, 루트 노드에서 모든 리프 노드로 가는 경로의 길이가 같다.



## B-Tree 동작 과정

### 1. 탐색 과정

B-Tree 는 root node 에서 탐색을 시작하여 하향식으로 탐색을 진행한다. 찾고자 하는 값이 K 라면 다음과 같은 과정을 거친다.

```tex
1. root node 에서 탐색을 시작
2. K 를 찾았다면 탐색 종료
3. K 와 node 의 Key 값을 비교해 알맞은 자식 노드로 내려간다.
4. 해당 과정을 리프 노드에 도달할 때까지 반복한다.
5. 리프 노드에서도 K 를 찾지 못한다면 트리에 값이 존재하지 않는 것이다.
```



### 2. 삽입 과정

B-Tree에 데이터를 삽입하는 과정은 탐색과는 다르게 상향식으로 진행된다. B-Tree에서의 데이터 삽입은 항상 리프 노드에서 시작된다.

```tex
1. 트리가 비어있다면 root node를 할당하고 K를 삽입한다.
2. 트리가 비어있지 않다면, 데이터를 넣을 적절한 리프 노드를 탐색한다.
3. leaf node에 데이터를 넣고 leaf node 가 적절한 상태에 있다면 종료한다.
4. leaf node 가 부적절한 상태에 있다면 분리한다.
```

이때, 적절한 상태란 해당 node의 데이터 개수가 허용 범위 안에 있는 것이다. 반대로 부적절한 상태란 해당 node 의 데이터 개수가 허용 범위를 벗어나 너무 많은 상태를 뜻한다.

#### 2.1 case 1. 분리가 일어나지 않는 경우

1. 데이터를 삽입할 리프 노드를 탐색하고, 해당 노드에 데이터를 삽입한다.
2. 해당 노드가 적절한 상태에 있다면, 삽입을 종료한다.



#### 2.2 case 2. 분리가 일어나는 경우

1. 데이터를 삽입할 leaf node 를 탐색하고, 해당 노드에 데이터를 삽입한다.
2. 해당 노드의 왼쪽 키들은 왼쪽 자식으로, 오른쪽 키들은 오른쪽 자식으로 분리된다.
3. 부모 노드를 검사해 부모 노드가 부적절한 상태에 있다면 위와 같은 분리를 반복한다.



### 3. 삭제 과정

B-Tree의 데이터 삭제 과정은 삽입하는 과정보다 조금 더 복잡하다. 우선 설명의 편의를 위해 다음과 같은 용어들을 임의로 정의한다.

**left_max = 현재 노드의 왼쪽 자식들 중 가장 큰 Key**

**right_max = 현재 노드의 오른쪽 자식들 중 가장 큰 Key**

**parent: 현재 노드를 가리키는 부모 노드의 자식 포인터 오른쪽에 있는 Key. 단, 마지막 자식 노드의 경우는 부모의 마지막 Key** 

**K : 삭제할 Key** 

#### 3.1 case 1. leaf node에서 삭제

- case1.1 leaf node에서 값을 삭제하더라도 최소 유지 개수 조건을 만족하는 경우

  ➡ 바로 node 삭제

- case1.2 leaf node에서 값을 삭제할 때, 최소 유지 개수를 만족하지 못하지만 바로 옆 sibling node들 에게 값을 빌려올 수 있는 경우



