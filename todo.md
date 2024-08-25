# TODO:

1. Identificar as colunas que vamos olhar
2. Definir as variaveis fuzzy para essas colunas

# Progress:

1. popularity, revenue, runtime, vote average

2. Podemos criar agora valores para essas variaveis, para isso vamos pegar alguns valores para conseguirmos analisar o universo, o membership e as variaveis em si

Basic data for us to create the fuzzy variables:

### Popularity:

- **Mean**: 21.49
- **Standard Deviation**: 31.82
- **Min**: 0.00
- **10th Percentile**: 1.28
- **Median (50%)**: 12.92
- **90th Percentile**: 48.82
- **Max**: 875.58

### Revenue:

- **Mean**: $82,260,640.64
- **Standard Deviation**: $162,857,100.19
- **Min**: $0.00
- **10th Percentile**: $0.00
- **Median (50%)**: $19,170,000.00
- **90th Percentile**: $227,634,600.00
- **Max**: $2,787,965,087.00

### Runtime (in minutes):

- **Mean**: 106.88 minutes
- **Standard Deviation**: 22.61 minutes
- **Min**: 0.00 minutes
- **10th Percentile**: 87.00 minutes
- **Median (50%)**: 103.00 minutes
- **90th Percentile**: 132.00 minutes
- **Max**: 338.00 minutes

### Vote Average:

- **Mean**: 6.09
- **Standard Deviation**: 1.19
- **Min**: 0.00
- **10th Percentile**: 4.90
- **Median (50%)**: 6.20
- **90th Percentile**: 7.30
- **Max**: 10.00

# Variaveis fuzzy

### 1. Popularity

**Categories**:

- **Extremely Popular**
- **Popular**
- **Normal**
- **Unpopular**

**Universe**: `[0, 1.28, 12.92, 48.82, 875.58]`

**Membership Functions**:

- **Extremely Popular**: Starts high after the 90th percentile (`48.82`) and is fully true at the max (`875.58`).
- **Popular**: Starts increasing from the median (`12.92`) and peaks around the 90th percentile (`48.82`).
- **Normal**: Fully true between the 10th percentile (`1.28`) and the median (`12.92`).
- **Unpopular**: Fully true near the minimum (`0`) and decreases after the 10th percentile (`1.28`).

### 2. Revenue

**Categories**:

- **Blockbuster**
- **Hit**
- **Average**
- **Flop**

**Universe**: `[0, 19,170,000, 82,260,640, 227,634,600, 2,787,965,087]`

**Membership Functions**:

- **Blockbuster**: Starts high near the 90th percentile (`227,634,600`) and is fully true at the max (`2,787,965,087`).
- **Hit**: Increases from the mean (`82,260,640`) and peaks around the 90th percentile (`227,634,600`).
- **Average**: Fully true between the 10th percentile (`19,170,000`) and the median (`82,260,640`).
- **Flop**: Fully true at the minimum (`0`) and decreases as it approaches the 10th percentile (`19,170,000`).

### 3. Runtime

**Categories**:

- **Very Long**
- **Long**
- **Medium**
- **Short**

**Universe**: `[0, 60, 103, 132, 338]`

**Membership Functions**:

- **Very Long**: Fully true at or above the 90th percentile (`132`) and extends to the maximum (`338`).
- **Long**: Starts from the median (`103`) and peaks around the 90th percentile (`132`).
- **Medium**: Fully true between the 10th percentile (`87`) and the median (`103`).
- **Short**: Fully true at or below the 10th percentile (`87`).

### 4. Vote Average

**Categories**:

- **Excellent**
- **Good**
- **Average**
- **Poor**

**Universe**: `[0, 4.9, 6.2, 7.3, 10]`

**Membership Functions**:

- **Excellent**: Starts from the 90th percentile (`7.3`) and is fully true at the max (`10`).
- **Good**: Fully true between the median (`6.2`) and the 90th percentile (`7.3`).
- **Average**: Fully true between the 10th percentile (`4.9`) and the median (`6.2`).
- **Poor**: Fully true near the minimum (`0`) and decreases after the 10th percentile (`4.9`).
