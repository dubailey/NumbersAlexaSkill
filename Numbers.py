"""
This is a simple alexa translation skill created by Duncan Bailey, utilising the Numbers Api and it takes
a number or random as input and tells either a math related, date related, year related, or trivial fact
based on that number or a random number.
"""

from __future__ import print_function
import urllib2

def get_fact(intent_type, number, random=False):
    """gets random or not random fact based on intent type and return a string
    intent_type = 'trivia', 'math', 'date', or 'year'"""
    if random == True:
        number = 'random'
    else:
        number = str(number)
    url = 'http://numbersapi.com/'+number+'/'+intent_type
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Numbers " \
                    "Please tell me a number or nothing at all for a random number that " \
                    "you would like to know a triva, year, date, or math fact about " \
                    "say something like, random trivia fact or " \
                    "math fact about four hundred and fifty five"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me a number or nothing at all for a random number that " \
                    "you would like to know a triva, year, date, or math fact about" \
                    "say something like random trivia fact or " \
                    "math fact about four hundred and fifty five"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Numbers"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_number_attributes(number):
    return {"number": number}


def get_number_fact_in_session(intent, session):
    """ Gets number fact and prepares the speech to reply to the
    user.
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'Numberz' in intent['slots']:
        if 'value' in intent['slots']['Numberz']:
            number = intent['slots']['Numberz']['value']
            session_attributes = create_number_attributes(number)
            speech_output = get_fact(card_title.lower(), number)
        else:
            session_attributes = create_number_attributes('Random Number')
            speech_output = get_fact(card_title.lower(), None, random=True)
        reprompt_text = "You can ask me for a trivia, math, date, or year fact about a number " \
                    "say something like random trivia fact or " \
                    "math fact about four hundred and fifty five"
    elif 'Datez' in intent['slots']:
        if 'value' in intent['slots']['Datez']:
            number = intent['slots']['Datez']['value']
            number = number[5:7]+'/'+number[8:]
            session_attributes = create_number_attributes(number)
            speech_output = get_fact(card_title.lower(), number)
        else:
            session_attributes = create_number_attributes('Random Date')
            speech_output = get_fact(card_title.lower(), None, random=True)
        reprompt_text = "You can ask me for a trivia, math, date, or year fact about a number " \
                    "say something like random trivia fact or " \
                    "math fact about four hundred and fifty five"
        
    else:
        speech_output = "I'm not sure what number you would like to know a fact about" \
                        "Please try again"
        reprompt_text = "I'm not sure what number you would like to know a fact about" \
                        "tell me a number or nothing at all for a random number that " \
                        "you would like to know a triva, year, date, or math fact about" \
                        "say something like random trivia fact or " \
                        "math fact about four hundred and fifty five"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))




# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Trivia":
        return get_number_fact_in_session(intent, session)
    elif intent_name == "Date":
        return get_number_fact_in_session(intent, session)
    elif intent_name == "Year":
        return get_number_fact_in_session(intent, session)
    elif intent_name == "Math":
        return get_number_fact_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
