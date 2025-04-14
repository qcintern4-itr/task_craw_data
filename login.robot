*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Variables ***
${BROWSER}    chrome
${URL}        https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/login/newLogin.jsp
${USERNAME}   optimususer
${PASSWORD}   9v7ouEVBAN1h^zHg3K

*** Test Cases ***
Login to eClinicalWorks
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    
    # Wait for username field and enter username
    Wait Until Element Is Visible    name=username
    Input Text    name=username    ${USERNAME}
    
    # Click next button to go to password screen
    Click Button    xpath=//button[contains(text(),'Next')]
    
    # Wait for password field and enter password
    Wait Until Element Is Visible    name=password
    Input Text    name=password    ${PASSWORD}
    
    # Click login button
    Click Button    xpath=//button[contains(text(),'Login')]
    
    # Wait for successful login (you may need to adjust this based on actual page elements)
    Wait Until Page Contains    eClinicalWorks    timeout=30s
    
    # Add a small delay to ensure page is fully loaded
    Sleep    5s
    
    # Close browser
    Close Browser 