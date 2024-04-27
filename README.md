# WON! Trading Room

## FYP Project

BSc (Hons) Computer Science with Artificial Intelligence

Ock Ju Won

Address: http://18.139.100.114:8501/

# 멀티쓰레딩 적용

프론트엔드 단에서 api 서버로 json request를 보낼때 멀티쓰레딩을 적용하였다.
EC2의 프리 티어 인스턴스의 사양 상, 1vCPU 밖에 사용할 수 없고, 효율적이고 빠르게 I/O 작업을 할수있도록 해보았다.
실제, threading을 적용시켰으나, 멀티쓰레딩 적용전보다 시간이 더 오래걸렸다.

그 이유로는 다음과 같이 추론된다.

1. GIL (Global Interpreter Lock)
   Python의 CPython 구현에서는 GIL이라는 메커니즘 때문에 한 번에 하나의 스레드만 Python 코드를 실행할 수 있습니다. CPU 바운드 작업(계산 집중적인 작업)의 경우, 멀티스레딩이 오히려 오버헤드만 증가시키고 성능 향상을 기대하기 어렵습니다.

2. 네트워크 지연과 I/O
   멀티스레딩은 I/O 바운드 작업에서는 일반적으로 성능 향상을 가져오지만, 네트워크 지연이나 서버의 응답 속도가 일관되지 않거나 서버가 여러 동시 요청을 처리하는 데 최적화되지 않았다면, 이로 인한 지연이 발생할 수 있습니다.

3. 스레드 관리 오버헤드
   많은 수의 스레드를 생성하고 관리하는 것 자체도 오버헤드를 발생시킵니다. 스레드가 너무 많으면 컨텍스트 스위칭 비용이 증가하고, 이는 전체 성능 저하로 이어질 수 있습니다.

개선 방안
적절한 스레드 수: 너무 많거나 적은 스레드 수가 아닌, 시스템과 작업에 적합한 스레드 수를 설정합니다.
비동기 프로그래밍 사용: Python의 asyncio와 같은 비동기 프로그래밍을 사용하여 I/O 바운드 작업을 더 효율적으로 처리할 수 있습니다.
프로파일링: 실제 작업 시간을 측정하여 병목 현상을 발견하고 개선합니다.
멀티프로세싱 고려: CPU 바운드 작업의 경우, multiprocessing 모듈을 사용해 병렬 처리를 고려할 수 있습니다. 이는 각 프로세스가 독립적인 메모리 공간을 가지므로 GIL의 제한을 받지 않습니다.
성능 문제를 좀 더 정밀하게 분석하려면 프로파일링을 통해 어떤 부분에서 병목 현상이 발생하는지 확인하는 것이 좋습니다. 필요하시면 프로파일링을 위한 코드 작성을 도와드릴 수 있습니다.
