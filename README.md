# KDT 과제 모음

Python, 자료구조, 알고리즘, 컴퓨터 기초와 HTML/CSS를 학습하며 작성한 과제 저장소다.

각 주제의 **개념 정리**, **직접 구현한 코드**, **실행 예제**를 함께 기록했다.

---

## 빠른 이동

- [과제 한눈에 보기](#과제-한눈에-보기)
- [자료구조](#자료구조)
- [알고리즘과 컴퓨터 기초](#알고리즘과-컴퓨터-기초)
- [웹 프로젝트](#웹-프로젝트)
- [실행 방법](#실행-방법)
- [폴더 구조](#폴더-구조)

## 학습 분야

| 분야 | 학습 내용 |
| :--- | :--- |
| **Python** | 클래스, 함수, 자료구조 직접 구현 |
| **자료구조** | 배열, 큐, 스택, 링크드 리스트, 트리, 힙, 해시 테이블 |
| **알고리즘** | 기본 정렬, 분할 정복 정렬, 시간·공간 복잡도 |
| **컴퓨터 기초** | 2진수, 보수, 정수와 부동 소수점 표현 |
| **Front-end** | 시멘틱 HTML, Grid, Flexbox, 반응형 웹, 애니메이션 |

---

## 과제 한눈에 보기

| 번호 | 주제 | 핵심 내용 | 결과물 |
| :---: | :--- | :--- | :---: |
| 01 | 배열·큐·스택 | 기본 선형 자료구조 직접 구현 | [문서](<./자료구조 조사 및 구현 과제.md>) · [코드](./DataStructure.py) |
| 02 | 단일 링크드 리스트 | 노드 연결, 삽입·삭제·탐색 | [폴더](./LinkedList) |
| 03 | 더블 링크드 리스트 | 양방향 연결과 정·역방향 순회 | [폴더](./DoubleLinkedList) |
| 04 | 트리·이진 탐색 트리 | 트리 순회와 BST 연산 | [폴더](./Tree) |
| 05 | 힙 | 최대·최소 힙과 Heapify | [문서](./Heap/Heap.md) · [실행](./Heap/main.py) |
| 06 | 해시 테이블 | Chaining과 Open Addressing | [종합 문서](<./Heap/Hash table.md>) |
| 07 | 정렬 알고리즘 | 기본 정렬과 분할 정복 정렬 | [폴더](./Sort) |
| 08 | 복잡도 | Big-O와 Python 리스트 연산 비용 | [문서](<./시간복잡도 와 공간복잡도.md>) |
| 09 | 숫자 표현 | 2진수, 보수, 부동 소수점 | [문서](<./컴퓨터의 숫자 표현 방식.md>) |
| 10 | 당산 한입지도 | HTML/CSS 반응형 맛집 웹사이트 | [웹사이트](<./나만의 맛집 리스트/index.html>) |

---

## 자료구조

<details>
<summary><strong>01. 배열 · 큐 · 스택</strong></summary>

### 학습 내용

배열, 큐, 스택이 필요한 이유와 동작 방식을 조사하고 Python 클래스로 직접 구현했다.

| 클래스 | 구현 기능 |
| :--- | :--- |
| `MyArray` | 데이터 추가, 조회, 수정, 삭제 |
| `MyQueue` | FIFO 기반 `enqueue()`, `dequeue()` |
| `MyStack` | LIFO 기반 `push()`, `pop()` |

### 바로가기

- [조사 및 구현 문서](<./자료구조 조사 및 구현 과제.md>)
- [Python 구현 코드](./DataStructure.py)

</details>

<details>
<summary><strong>02. 단일 링크드 리스트</strong></summary>

### 학습 내용

노드가 다음 노드를 참조하는 단일 링크드 리스트를 구현했다. 터미널에서 삽입, 삭제, 검색과 노드 연결 상태를 직접 확인할 수 있다.

### 구현 기능

- 맨 앞·맨 뒤 노드 삽입
- 원하는 인덱스에 노드 삽입
- 값으로 노드 삭제 및 검색
- 인덱스로 데이터 조회
- 전체 연결 구조 출력

### 바로가기

- [상세 학습 문서](./LinkedList/Linked-list.md)
- [완성 코드](./LinkedList/linked_list.py)
- [연습용 스켈레톤 코드](./LinkedList/linked_list_skeleton.py)
- [터미널 시각화 프로그램](./LinkedList/main.py)

### 실행

```bash
cd LinkedList
python3 main.py
```

</details>

<details>
<summary><strong>03. 더블 링크드 리스트</strong></summary>

### 학습 내용

각 노드가 이전 노드와 다음 노드를 모두 참조하는 구조를 구현했다. 정방향·역방향 순회와 각 노드의 `prev`, `value`, `next` 정보를 확인할 수 있다.

### 바로가기

- [함수 설명 문서](./DoubleLinkedList/double_linked_list_함수설명.md)
- [완성 코드](./DoubleLinkedList/double_linked_list.py)
- [연습용 스켈레톤 코드](./DoubleLinkedList/double_linked_list_skeleton.py)
- [터미널 시각화 프로그램](./DoubleLinkedList/main.py)

### 실행

```bash
cd DoubleLinkedList
python3 main.py
```

</details>

<details>
<summary><strong>04. 트리 · 이진 탐색 트리</strong></summary>

### 학습 내용

- 트리의 계층 구조와 주요 용어
- 전위·중위·후위 순회
- 이진 트리의 종류
- 이진 탐색 트리의 삽입, 탐색, 삭제
- 연산별 시간 복잡도

### 바로가기

- [트리 학습 문서](./Tree/트리.md)
- [이진 트리·이진 탐색 트리 문서](<./Tree/이진트리, 이진탐색트리.md>)

</details>

<details>
<summary><strong>05. 최대 힙 · 최소 힙</strong></summary>

### 학습 내용

완전 이진 트리를 배열로 표현하는 방법을 학습하고 최대 힙과 최소 힙을 구현했다. `heapify_up`, `heapify_down` 과정을 터미널 트리로 시각화했다.

### 구현 기능

- 최대 힙과 최소 힙 삽입
- 루트 노드 삭제
- 상향·하향 Heapify
- 배열과 트리 구조 출력
- 부모·자식 인덱스 관계 출력

### 바로가기

- [힙 학습 문서](./Heap/Heap.md)
- [최대 힙 구현](./Heap/MaxHeap.py)
- [최소 힙 구현](./Heap/MinHeap.py)
- [힙 터미널 시각화](./Heap/main.py)

### 실행

```bash
cd Heap
python3 main.py
```

</details>

<details>
<summary><strong>06. 해시 테이블</strong></summary>

### 학습 내용

- 해시 함수와 Key-Value 구조
- Direct Address Table과 해시 테이블 비교
- 충돌이 발생하는 이유
- Chaining
- Open Addressing
- Linear Probing
- Python `dict`와 해시 테이블의 관계

### 바로가기

- [해시 테이블 종합 정리](<./Heap/Hash table.md>)
- [Chaining 충돌 해결 방식](./Heap/Chaining.md)
- [Linear Probing 충돌 해결 방식](<./Heap/Linear Probing.md>)

</details>

---

## 알고리즘과 컴퓨터 기초

<details>
<summary><strong>07. 정렬 알고리즘</strong></summary>

### 구현 알고리즘

| 분류 | 알고리즘 |
| :--- | :--- |
| 기본 정렬 | 버블 정렬, 선택 정렬, 삽입 정렬 |
| 분할 정복 | 병합 정렬, 퀵 정렬 |

동일한 난수 데이터를 사용해 각 정렬 알고리즘의 실행 시간을 비교할 수 있도록 구성했다.

### 바로가기

- [기본 정렬 알고리즘 문서](./Sort/기본_정렬_알고리즘_정리.md)
- [기본 정렬 구현](./Sort/basic_sort.py)
- [분할 정복 정렬 구현](./Sort/divide_conquer.py)
- [성능 비교 프로그램](./Sort/main.py)

### 실행

```bash
cd Sort
python3 main.py
```

</details>

<details>
<summary><strong>08. 시간 복잡도 · 공간 복잡도</strong></summary>

Big-O 표기법을 기준으로 알고리즘의 실행 시간과 메모리 사용량이 입력 크기에 따라 어떻게 증가하는지 정리했다.

### 다룬 복잡도

`O(1)` · `O(log n)` · `O(n)` · `O(n log n)` · `O(n²)`

Python 리스트의 `append()`, `insert()`, `pop()`, `remove()`, `sort()` 연산 비용도 예제로 비교했다.

- [시간 복잡도와 공간 복잡도 문서](<./시간복잡도 와 공간복잡도.md>)

</details>

<details>
<summary><strong>09. 컴퓨터의 숫자 표현 방식</strong></summary>

### 학습 내용

- 컴퓨터가 2진수를 사용하는 이유
- 비트와 바이트
- 부호 있는 정수와 부호 없는 정수
- 1의 보수와 2의 보수
- IEEE 754 부동 소수점
- 부동 소수점 오차가 발생하는 이유

- [컴퓨터의 숫자 표현 방식 문서](<./컴퓨터의 숫자 표현 방식.md>)

</details>

---

## 웹 프로젝트

### 10. 당산 한입지도

영등포구 당산동 주변의 점심 맛집, 저녁 맛집과 카페를 소개하는 반응형 웹사이트다.

| 구분 | 내용 |
| :--- | :--- |
| 개발 방식 | HTML5, CSS3 |
| 페이지 | 전체 추천, 점심, 카페·저녁 |
| 레이아웃 | CSS Grid, Flexbox |
| 반응형 | PC, 태블릿, 모바일 |
| 인터랙션 | Hover, Transition, Transform, Animation |
| 외부 연결 | 음식점별 Google 지도 검색 |

### 바로가기

- [웹사이트 실행](<./나만의 맛집 리스트/index.html>)
- [프로젝트 상세 README](<./나만의 맛집 리스트/README.md>)

---

## 실행 방법

### Python 예제

Python 3 외에 별도의 외부 패키지는 필요하지 않다.

```bash
python3 --version
cd 실행할_과제_폴더
python3 main.py
```

### 웹 프로젝트

브라우저에서 [index.html](<./나만의 맛집 리스트/index.html>)을 직접 열거나 로컬 서버로 실행한다.

```bash
cd "나만의 맛집 리스트"
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000`에 접속한다.

---

## 폴더 구조

```text
과제/
├── DoubleLinkedList/        # 더블 링크드 리스트
├── Heap/                    # 힙과 해시 테이블
├── LinkedList/              # 단일 링크드 리스트
├── Sort/                    # 정렬 알고리즘
├── Tree/                    # 트리와 이진 탐색 트리
├── images/                  # 문서 이미지
├── 나만의 맛집 리스트/       # HTML/CSS 웹 프로젝트
├── DataStructure.py         # 배열·큐·스택
├── 시간복잡도 와 공간복잡도.md
├── 자료구조 조사 및 구현 과제.md
├── 컴퓨터의 숫자 표현 방식.md
└── README.md
```

## 학습 목표

- 자료구조가 어떤 문제를 해결하기 위해 만들어졌는지 이해한다.
- 삽입, 삭제, 탐색 과정과 참조 관계를 코드로 구현한다.
- 시간 복잡도와 공간 복잡도를 고려해 구현 방식을 비교한다.
- 알고리즘의 동작 과정을 문서와 시각화 예제로 설명한다.
- HTML과 CSS로 여러 페이지를 갖는 반응형 웹사이트를 제작한다.

## 참고 사항

- 기존 과제 코드, 문서와 하위 README는 그대로 유지한다.
- 일부 폴더에는 완성 코드와 연습용 스켈레톤 코드가 함께 포함되어 있다.
- 문서와 웹 프로젝트의 이미지는 학습 및 포트폴리오 목적으로 정리했으며 각 이미지의 권리는 원저작자에게 있다.
