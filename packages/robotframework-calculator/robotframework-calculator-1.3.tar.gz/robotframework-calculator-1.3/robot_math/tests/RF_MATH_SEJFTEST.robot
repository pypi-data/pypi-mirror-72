*** Settings ***
Documentation    ROBOT_MATH self robot tests
Library          BuiltIn
Library          Collections
Library          robot_math.ROBOT_MATH

*** Test Cases ***
Packet test
    [Tags]  Packet
    [Template]  executor
    PACKET_OPERATION   10M==80m
    PACKET_OPERATION   10M==9M    deviation=10%
    PACKET_OPERATION   10M>80m     expected=FAIL
    PACKET_OPERATION   10M<80m     expected=FAIL  reason=My reason to fail
    PACKET_OPERATION   100M+10%
    PACKET_OPERATION   100M + 10%
    PACKET_OPERATION   100M - 10%
    PACKET_OPERATION   10M+5M


Time test
    [Tags]  Time
    [Template]  executor
    TIME_OPERATION   1h==60m
    TIME_OPERATION   1h>=60m
    TIME_OPERATION   1h<=60m
    TIME_OPERATION   1h==59m  expected=FAIL
    TIME_OPERATION   1h==54m  deviation=10%
    TIME_OPERATION   1h==54m  deviation=0.1
    TIME_OPERATION   1h==53m  deviation=10%  reason=My reason  expected=FAIL
    TIME_OPERATION   1h>59m
    TIME_OPERATION   59m<1h
    TIME_OPERATION   1h+20m
    TIME_OPERATION   12h+50%
    TIME_OPERATION   12h - 50%

*** Keywords ***
executor
    [Arguments]  ${keyword}  ${expression}  ${expected}=PASS  ${deviation}=${EMPTY}  ${reason}=${EMPTY}
    ${st}=  run keyword and ignore error  ${keyword}  ${expression}  deviation_str=${deviation}  reason=${reason}
    run keyword if  '${st}[0]' != '${expected}'  fail  Expression ${expression} failed
    set test message  Expression ${expression} completed with: ${st}[1] (Expected: ${expected} vs. Real: ${st}[0])\n  append=${TRUE}