*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String

*** Variables ***
${BROWSER}    chrome
${URL}        https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/login/newLogin.jsp
${USERNAME}   optimususer
${PASSWORD}   9v7ouEVBAN1h^zHg3K
${CONFIG_FILE}    config.py

*** Test Cases ***
Login to eClinicalWorks
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    
    # Wait for username field and enter username
    Wait Until Element Is Visible    name=doctorID
    Input Text    name=doctorID    ${USERNAME}
    
    # Click next button to go to password screen
    Click Button    xpath=//*[@id="nextStep"]
    
    # Wait for password field and enter password
    Wait Until Element Is Visible    name=passwordField
    Input Text    name=passwordField   ${PASSWORD}
    
    # Click login button
    Click Button    xpath=//*[@id="Login"]
    
    # Click Agree button
    Sleep   5s
    Wait Until Element Is Visible    id=showDisclaimerModal
    Click Button    xpath=//*[@id="agreeBtn"]
    
    # Get X-CSRF-Token from meta tag
    ${csrf_token}=    Execute JavaScript    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
    
    # Get Cookie from browser
    ${cookies}=    Get Cookies
    ${jsessionid}=    Get Cookie Value    JSESSIONID
    ${affinity}=    Get Cookie Value    ApplicationGatewayAffinity
    ${affinity_cors}=    Get Cookie Value    ApplicationGatewayAffinityCORS
    
    # Format cookie string
    ${cookie_string}=    Set Variable    JSESSIONID=${jsessionid}; ApplicationGatewayAffinityCORS=${affinity_cors}; ApplicationGatewayAffinity=${affinity}
    
    # Update config.py with new values
    #Update Config File    ${csrf_token}    ${cookie_string}
    log     ${csrf_token}       ${cookie_string}
    
    # Close browser
    Close Browser

*** Keywords ***
Update Config File
    [Arguments]    ${csrf_token}    ${cookie_string}
    ${config_content}=    Get File    ${CONFIG_FILE}
    
    # Update X-CSRF-Token in API_HEADERS_TABLE2
    ${config_content}=    Replace String    ${config_content}
    ...    "X-CSRF-Token": "771f0f6e-4b11-4137-b6f0-864702b11896"
    ...    "X-CSRF-Token": "${csrf_token}"
    
    # Update X-CSRF-Token in API_HEADERS_TABLE3
    ${config_content}=    Replace String    ${config_content}
    ...    "X-CSRF-Token": "519f25c9-a927-4eb1-8afe-013622b83047"
    ...    "X-CSRF-Token": "${csrf_token}"
    
    # Update Cookie in API_HEADERS_TABLE2
    ${config_content}=    Replace String    ${config_content}
    ...    "Cookie": "JSESSIONID=F2D544C4AD6E11D2BAFC9CDC157FC033; ApplicationGatewayAffinityCORS=124274af792cba06a0461a764f502f20; ApplicationGatewayAffinity=124274af792cba06a0461a764f502f20"
    ...    "Cookie": "${cookie_string}"
    
    # Update Cookie in API_HEADERS_TABLE3
    ${config_content}=    Replace String    ${config_content}
    ...    "Cookie": "JSESSIONID=310BE3CAFD63DA959F997972A7F3DB8D; ApplicationGatewayAffinityCORS=55188ab720fd86c8c53f4d3764729277; ApplicationGatewayAffinity=55188ab720fd86c8c53f4d3764729277"
    ...    "Cookie": "${cookie_string}"
    
    Create File    ${CONFIG_FILE}    ${config_content} 