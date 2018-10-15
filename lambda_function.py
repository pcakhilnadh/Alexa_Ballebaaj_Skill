import json
import random

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
    msg="Ballebaj Instruction. "
    msg+="We , Team 'Gendabaaj' has finished batting. Now, You need to chase our score to win. "
    msg+="You have got 6 overs and 3 wickets to beat us. "
    msg+="You need to pick and say a number from 0 to 6 which you think you could possibly take in every bowl. It is called Bellebaj shot. "
    msg+="Similarly, We 'Gendabaaj', the bowling team will also select the bowling number called Gendabaaj bowl. "
    msg+="If both numbers happens to be same . You will loose a wicket. "
    msg+="If Both numbers are different, then you will get that much number of Score. "
    msg+="Say 'Instruction' to Repeat. Say 'Continue' to Start Playing Ballebaj  Game "

    return conversation("Instruction", msg,session_attributes)
def continueIntent(event,context):
    GendabaajScore=random.randint(50,180)
    session_attributes=setStartSession(event,context)
    session_attributes['GendabaajScore']=GendabaajScore
    msg="Lets Play Ballebaj Game. "
    msg+="We, Gendabaaj has finished batting. You need to attain "+str(GendabaajScore)+" Score to beat us from 6 overs. "
    msg+="Select your Ballebaj Shot from 0 to 6 on every bowl. "
    msg+="Lets Begin ! Are you Ready to  chase us ? "
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
