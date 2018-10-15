import json

# Builders
def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

#Responses
def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


#Set Starting Session
def setStartSession(event,context):
    if 'attributes' in event['session']:
        session_attributes=event['session']['attributes']
        if 'sessionStatus' in session_attributes:
            if 'sessionStatus' is True:
                pass
        else:
            session_attributes['sessionStatus']=True
    else:
        event['session']['attributes']={}
        session_attributes=event['session']['attributes']
        session_attributes['sessionStatus']=True
    return session_attributes

#Custom Intent
def instructionIntent(event,context):
    session_attributes=setStartSession(event,context)
    msg="Instruction "+str(session_attributes['sessionStatus'])
    return conversation("Instruction", msg,session_attributes)
def continueIntent(event,context):
    session_attributes=setStartSession(event,context)
    msg="Continue "+str(session_attributes['sessionStatus'])
    return conversation("GameBegins", msg,session_attributes)

#Routing
def intent_router(event, context):
    intent = event['request']['intent']['name']
    if intent == "Instruction":
        return instructionIntent(event,context)
    if intent == "Continue":
        return continueIntent(event,context)

# On Launch
def on_launch(event, context):
    msg="Welcome to Ballebaj Game. You need to bat and attain a certain target to win the game. You have got 6 overs and 3 wickets. "
    msg+="If you want to listen to Instruction say 'Instruction' else say 'Continue'"
    session_attributes=setStartSession(event,context)
    return conversation("Ballebaj Launch", msg,session_attributes)

# Main - Entry
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
