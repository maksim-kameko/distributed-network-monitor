*** Settings ***
Library  RequestsLibrary
Library  Collections

*** Variables ***
${BASE_URL}  http://127.0.0.1:8000
${IP_TO_CHECK}  8.8.8.8

*** Test Cases ***
Check If Network Monitor API Is Alive
	[Documentation]  Checks if endpoint API returning status 200
	Create Session  monitor  ${BASE_URL}
	${response}=  Get On Session  monitor  /${IP_TO_CHECK}
	Should Be Equal As Integers  ${response.status_code}  200

Verify Google DNS Status Is Online
    [Documentation]    Checks if ping output contains information about received bytes
    Create Session    monitor    ${BASE_URL}
    ${response}=      GET On Session    monitor    /${IP_TO_CHECK}
    ${json}=          Set Variable    ${response.json()}
    Should Contain    ${json['result']}    64 bytes from
