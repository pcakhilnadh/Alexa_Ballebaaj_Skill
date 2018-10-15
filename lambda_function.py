import json
import random

"""
Deveoped by Pc
Current Version : 1.0 v

Features Expected in Next Update
1. gameplay modifed to 3 wickets and 6 overs
2. Special music and sounds if person got Duck , centuary or fifty.

"""
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

#Built-In Intents
def fallbackIntent(event,context):
    session_attributes=setStartSession(event,context)
    return conversation("FallBack","That was an Error. Say 'instruction' to listen to instructions.",session_attributes)
def helpIntent(event,context):
    session_attributes=setStartSession(event,context)
    return conversation("Help","help Intent",session_attributes)
def stopIntent(event,context,msg=''):
    msg+=" You Lost the Game. Better Luck Next Time"
    return statement("End",msg)
def winner(event,context,msg=''):
    msg+=" Congratulations ! You won the game."
    return statement("Winner",msg)

#Custom Intent
def instructionIntent(event,context):
    session_attributes=setStartSession(event,context)
    msg="Ballebaj Instruction. "
    msg+="We , Team 'Gendabaaj' has finished batting. Now, You need to chase our score to win. "
    msg+="You have got 2 overs and 1 wicket to beat us. "
    msg+="You need to pick and say a number from 0 to 6 which you think you could possibly take in every bowl. It is called Ballebaaj runs. "
    msg+="Similarly, We 'Gendabaaj', the bowling team will also select the bowling number called Gendabaaj bowl. "
    msg+="If both numbers happens to be same . You will loose a wicket. "
    msg+="If Both numbers are different, then you will get that much number of runs. "
    msg+="Say 'Instruction' to Repeat. Say 'Continue' to Start Playing Ballebaj  Game "
    return conversation("Instruction", msg,session_attributes)

def continueIntent(event,context):
    GendabaajScore=random.randint(30,55)
    session_attributes=setStartSession(event,context)
    session_attributes['GendabaajScore']=GendabaajScore
    msg="Lets Play Ballebaj Game. "
    msg+="We, Gendabaaj has finished batting. You need to attain "+str(GendabaajScore)+" Score to beat us from 2 overs. "
    msg+="Select your Ballebaj runs from 0 to 6 on every bowl. "
    msg+="Lets Begin ! Are you Ready to  chase us ? Say start "
    return conversation("GameBegins", msg,session_attributes)

def gameBeginIntent(event,context):
    session_attributes=setStartSession(event,context) #Get Session
    if 'BallebajScore' not in session_attributes:
        session_attributes['BallebajScore']=0
        session_attributes['over']=1
        session_attributes['bowl']=1
        session_attributes['bat']={}
        session_attributes['bat']['1']={}
        session_attributes['bat']['1']['status']="BATING"
        session_attributes['bat']['1']['score']=0
        session_attributes['bat']['1']['bowls']=0
    msg=str(session_attributes['bowl'])+" Bowl of "+str(session_attributes['over'])+" Over. "
    msg+=" Belle Bele Ballebaj, Say 'Runs' : "
    return conversation("Ballebaj Begins", msg,session_attributes)

def ballebajShotIntent(event,context):
    session_attributes=setStartSession(event,context) #Get Session
    slot=event['request']['intent']['slots']['runs']
    if 'value' in slot:
        runs=int(slot['value'])
        if runs not in range(0,7):
            msg="Please choose a runs from 0 to 6 from a bowl."
        else:
            BowlRun=random.randint(0,6)
            msg="Gendabaaj Bowled score was "+str(BowlRun)+". "
            if BowlRun == runs:
                msg+="Sorry You Lost a Wicket. "
                return stopIntent(event,context,msg)
            else:
                msg+="That was a nice shot. You got "+str(runs)+" Runs. "
                session_attributes['BallebajScore']+=runs
                session_attributes['bat']['1']['score']+=runs
                session_attributes['bat']['1']['bowls']+=1
                session_attributes['bowl']+=1
                if session_attributes['BallebajScore'] >session_attributes['GendabaajScore']:
                    msg+=" You beat us by "+str(session_attributes['BallebajScore']-session_attributes['GendabaajScore'])+" runs."
                    return winner(event,context,msg)
                if session_attributes['bowl']%6 == 0:
                    session_attributes['over']+=1
                    session_attributes['bowl']=1
                    if session_attributes['over'] <=2:
                        msg+="Ballebaaj Team scored "+str(session_attributes['BallebajScore'])+" runs in Total."
                        msg+=" You need "+str(session_attributes['GendabaajScore']-session_attributes['BallebajScore']+1)+" more runs needed to win"
                    else:
                        msg+="2 overs are over"
                        msg+="Ballebaaj Team scored "+str(session_attributes['BallebajScore'])+" runs in Total."
                        return stopIntent(event,context,msg)
                else:
                    msg+="Bowl "+str(session_attributes['bowl'])+" of "+str(session_attributes['over'])+" Over. "
                    msg+=" Belle Bele Ballebaj, Say 'Runs' : "
    else:
        msg="Please say 'Runs 5' if you expect to take 5 runs in the bowl."
    return conversation("Ballebaj Shot",msg,session_attributes)

#Routing
def intent_router(event, context):
    intent = event['request']['intent']['name']
    if intent == "Instruction":
        return instructionIntent(event,context)
    if intent == "Continue":
        return continueIntent(event,context)
    if intent == "GameBegins":
        return gameBeginIntent(event,context)
    if intent == "BallebajShot":
        return ballebajShotIntent(event,context)

    if intent=="AMAZON.FallbackIntent":
        return fallbackIntent(event,context)
    if intent=="AMAZON.HelpIntent":
        return helpIntent(event,context)
    if intent=="AMAZON.StopIntent":
        return stopIntent(event,context)

# On Launch
def on_launch(event, context):
    msg="Welcome to Ballebaaj Game. You need to bat and attain a certain target to win the game. You have got 2 overs and 1 wickets. "
    msg+="If you want to listen to Instruction say 'Instruction' else say 'Continue'"
    session_attributes=setStartSession(event,context)
    return conversation("Ballebaaj Launch", msg,session_attributes)

# Main - Entry
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
