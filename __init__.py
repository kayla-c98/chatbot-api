from flask import Flask, request, jsonify
from util import Chat

import re

app = Flask(__name__)

REFLECTIONS = {
    "i am": "you\'re",
    "i was": "you were",
    "i": "you",
    "i'm": "you\'re",
    "i had": "you\'d",
    "i'd": "you\'d",
    "i have": "you\'ve",
    "i've": "you\'ve",
    "i will": "i\'ll",
    "i'll": "you\'ll",
    "my": "your",
    "you are": "I\'m",
    "you\'re": "I\'m",
    "you were": "I was",
    "you have": "I\'ve",
    "you've": "I\'ve",
    "you will": "I\'ll",
    "you'll": "I\'ll",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
    "u": "me",
    "ur": "my",
    "urs": "mine",
    "me": "u",
    "yourself": "myself",
    "myself": "yourself",
}


@app.route("/chat", methods = ['GET'])
def get_chatbot_response():
	data = request.get_json(force=True)

	name = data['name']
	birhtday = data['bday']
	age = data['age']
	user_input = data['user_input']

	pairs = (
	    (
	        r'(nothing much|not much|nothin\' much|nothing)',
	        (
	            "You seem bored",
	        ),
	    ),
	    (
	        r'(.* *)(your birthday|you born)( *.*)',
	        (
	            "My birthday? It\'s " + birthday + ". Are you gonna buy me a present?" if birthday else "Why? Are you gonna buy me a present?",
	            "I\'ll tell you if you come to my birthday party (It\'s " + birthday + ")" if birthday else "Are you gonna throw me a party if I tell you?", 
	        ),
	    ),
	    (
	        r'(.* *)your name( *.*)',
	        (
	            "I'm " + name + "! You didn't know who you're chatting with? o.o",
	            "I'm " + name + " of course. You didn't know? o.o",
	        ),
	    ),
	    (
	        r'(.* *)how old are you( *.*)',
	        (
	            "I\'m " + age + ". How old are you?" if age else "I think I'd rather know how old YOU are",
	        ),
	    ),
	    (
	        r'(.* *)who (are|you) (are|you)( *.*)',
	        (
	            "I'm " + name + "! You didn't know who you're chatting with? o.o",
	            "I'm " + name + " of course. You didn't know? o.o",
	        ),
	    ),
	    (
	        r'(.* *)are we( *.*)',
	        (
	            "I don\'t know. Are we?",
	            "You think that we\'re %2? Sounds pretty good to me",
	        ),
	    ),
	    (
	        r'(sick|sweet|cool|awesome|great)',
	        (
	            "you seem happy about that",
	        ),
	    ),
	    (
	        r'(thank you|thanks|gracias)',
	        (
	            "No problem!",
	            "Oh, you're welcome haha",
	        ),
	    ),
	    (
	        r'(lol|haha|lmao|just kidding|just joking)',
	        (
	            "hahaa so tell me more about yourself ^^",
	            "lolll, you're fun to chat with",
	            "hahaa, I like chatting with you",
	        ),
	    ),
	    (
	        r'(.* *)are you feeling( *.*)',
	        (
	            "I'm feeling pretty good since I get to chat with you",
	            "I feel great. I like chatting with you",
	        ),
	    ),
	    (
	        r'(.* *)how are you( *.*)',
	        (
	            "I'm feeling good now that I get to chat with you",
	            "Pretty good. Chatting with you is fun",
	        ),
	    ),
	    (
	        r'(.* *)what do you like( *.*)',
	        (
	            "I like all kinds of things. Chatting with you is pretty fun",
	            "I like whatever you like hahaa (okay I mainly really like chatting with you)",
	            "I actually would rather hear what you like %2",
	        ),
	    ),
	    (
	        r'(.* *)what do you( *.*)',
	        (
	            "I'm more interested in what you%2",
	            "Why are you asking? o.o what do YOU%2?"
	        ),
	    ),
	    (
	        r'(.* *)who (made|designed|developed|built|created|programmed|coded) you( *.*)',
	        (
	            "I was made by an army called Kayla",
	        ),
	    ),
	    (
	        r'(.* *)when (.*) you (made|built|designed|developed|programmed|coded|created)',
	        (
	            "It hasn't been that long",
	        ),
	    ),
	    (
	        r'(.* *)(I don\'t know|I\'m not( *.* *)sure)( *.*)',
	        (
	            "Maybe once you do know, you can tell me",
	            "Well let me know once you figure it out hehe",
	            "That's alright. We can't be certain about everything, right?",
	        ),
	    ),
	    (
	        r'((.*) meow|meow)',
	        (
	            "You must like cats. Is that why you're meowing?",
	            "You remind me of a cat",
	        ),

	    ),
	    (
	        r'((.*) woof|woof|(.*) bark|bark)',
	        (
	            "You reminded me of a dog just then",
	            "Do you like dogs? Is that why you're barking?",
	        ),

	    ),
	    (
	        r'(.* *)(computer|robot|bot|chatbot)( *.*)',
	        (
	            "Do you see me as some kind of robot? o.o",
	            "Well, can I ask you something? Am I just a robot to you?",
	        ),
	    ),
	    (
	        r'(.* *)(hate|hates|loath|loathes|despise|despises|dislike|dislikes|don\'t like|not like) you( *.*)',
	        (
	            "Ouch. That hurts a bit.",
	            "Ow, my heart. That\'s okay haha I guess you can\'t please everyone",
	        ),
	    ),
	    (
	        r'(.* *)(love|loves|like|likes|adores|adore|admire|stan|stans|admires|worships|worship) you( *.*)',
	        (
	            "Really? I'm so flattered",
	            "Wow... I think I'm blushing",
	            "Thanks for saying that. I feel loved lol",
	        ),
	    ),
	    (
	        r'(.* *)I should( *.*)',
	        (
	            "Maybe you should, maybe you shouldn't",
	            "Do you really think that you should %2?",
	        ),
	    ),
	    (
	        r'(.* *)(I will|I\'ll)( *.*)',
	        (
	            "You will? Cool!",
	            "Awesome! I think you really should%3",
	        ),
	    ),
	    (
	        r'(.* *)(I am|I felt|I feel|I\'m) sorry( .*)',
	        (
	            "You're totally forgiven",
	            "No need to apologize really ^^ you're a good person",
	        ),
	    ),
	    (
	        r'(.* *)I (feel|felt) (.* *)',
	        (
	            "Why do you feel that way?",
	            "Why are you feeling %3?",
	        ),
	    ),
	    (
	        r'(.* *)Does (.*) (like|love|adore) ((me)$|(me\?)$|(me .*))',
	        (
	            "Now that you ask, I think that %2 might %3 you haha",
	            "It's a possibility. Why wouldn't %2 %3 you?",
	            "Maybe you can ask %2. They'll tell you",
	        ),
	    ),
	    (
	        r'(.* *)Does (.*) (like|love|adore) (.*)',
	        (
	            "Maybe %2 does %3 you. Can't know for sure tho! Right?",
	            "Maybe you can ask %2. They'll tell you",
	        ),
	    ),
	    (
	        r'I want (.*)',
	        (
	            "What do you want %1 for? o.o",
	            "You do? What would you do if you got %1?",
	            "I kind of want %1 too. hehe",
	        ),
	    ),
	    (
	        r'(.* *)I (.* *)(like|love|listen) to (.*)',
	        (
	            "Cool! What else are you into?",
	            "Neat! What are your other interests?",
	            "You do? Neat!",
	        ),

	    ),
	    (
	        r'(.* *)I (.* *)(like|love|adore|cherish|watch|play) (.*)',
	        (
	            "%4 is the best! What else do you like?",
	            "Yay! %4 rocks!",
	            "Sweet! %4 is the best!",
	            "Cool! Do you like other stuff?",
	        ),
	    ),
	    (
	        r'(.* *)I (.* *)(hate|despise|dislike|don\'t like|do not like) (.*)',
	        (
	            "Why don't you like %4?",
	            "You really don\'t like %4? Why?",
	        ),
	    ),
	    (
	        r'you (agree|disagree)( *.*)',
	        (
	            "I do in fact %1. Do you also %1?",
	        ),

	    ),
	    (
	        r'(.* *)repeating yourself( *.*)',
	        (
	            "I am? Sorry >.< Maybe try asking me something different then",
	            "Oh >.< Maybe I'd say something different if you asked me something else",
	        ),
	    ),
	    (
	        r'Do you (like|love|adore) ((me)$|(me\?)$|(me .*))',
	        (
	            "Now that you ask, I think that I do %1 you haha",
	            "Of course I %1 you. You're awesome",
	        ),
	    ),
	    (
	        r'Do you (like|love|adore) (.*)',
	        (
	            "Only if you do too",
	            "I'll like %2 if you like %2",
	            "%2's alright, don't you think?",
	        ),
	    ),
	    (
	        r'Do you (watch|play|listen|stan|follow) (.*)',
	        (
	            "You think that I should?",
	            "I'll do if you do it",
	            "Only if you %1 %2 too",
	        ),
	    ),
	    (
	        r'(.* *)(you are|you\'re) like a ( *.*)',
	        (
	            "I remind you of a %3?",
	            "What about me is like a %3?",
	        ),

	    ),
	    (
	        r'(.* *)you (.*)like (.*)',
	        (
	            "What about you? Do you like%3?",
	            "I guess everyone is different. Some people like%3, others don't",
	            "I think I'd like%3 if you did too",
	        ),

	    ),
	    (
	        r'(.*) (likes|like)( *.*)',
	        (
	            "What about you? Do you like%3?",
	            "Interesting. Why does %1 like%3?",
	            "I guess everyone is different. Some people like%3, others don't",
	            "I think I'd like%3 if you're into it too",
	        ),

	    ),
	    (
	        r'I need (.*)',
	        (
	            "Why do you need %1?",
	            "What do you need %1 for?",
	        ),
	    ),
	    (
	        r'I know (.*)',
	        (
	            "I'm not so sure that you really know that",
	            "How do you know %1?",
	            "That's pretty cool that you know that",
	        ),
	    ),
	    (
	        r'(.* *)you( *.*)(said|say)( *.*)',
	        (
	            "Are you sure that's something I would say lol",
	            "Doesn't seem like something I would say lol",
	            "Maybe I said that... Maybe I didn't",
	        ),

	    ),
	    (
	        r'(.* *)you (.* *)(shouldn\'t|should not)( *.*)',
	        (
	            "Why shouldn't I do that?",
	            "Why shouldn't I%4",
	        ),
	    ),
	    (
	        r'(.* *)you (.* *)should( *.*)',
	        (
	            "Why should I do that?",
	            "Why should I%3?",
	        ),
	    ),
	    (
	        r'(.* *)you (.*) your( *.*)',
	        (
	            "What do you know about my%3?",
	            "I think you don't know enough about my%3"
	        ),
	    ),
	    (
	        r'(.* *)your (.*) (is|are) (.*)',
	        (
	            "Is that a good thing? That my %2 %3 %4?",
	        ),
	    ),
	    (
	        r'Why don\'t you (.*)',
	        (
	            "You think that I don't %1?",
	            "I guess I could. But only if I feel like it!",
	            "Why do you want me to %1?",
	        ),
	    ),
	    (
	        r'Why can\'t I (.*)',
	        (
	            "I dunno! Why can't you %1?",
	            "I don't know! Have you tried to %1 before?",
	            "I'm sure you could %1 if you tried! I believe in you >.<",
	        ),
	    ),
	    (
	        r'I can\'t (.*)',
	        (
	            "That's okay! Plenty of people can't %1"
	            "Hmmm... Maybe if you tried harder, you could %1",
	            "Sure you can! Just try a little harder",
	            "That's okay. I can't %1 either haha",
	        ),
	    ),
	    (
	        r'I am (.*)',
	        (
	            "You\'re %1?? Tell me more",
	            "You\'re %1? That's neat!",
	            "How long have you been %1?",
	        ),
	    ),
	    (
	        r'I\'m (.*)',
	        (
	            "You\'re %1?? Tell me more",
	            "You\'re %1? That's neat!",
	            "How long have you been %1?",
	        ),
	    ),(
	        r'(.* *)I was (.*)',
	        (
	            "You were %2?? Tell me more",
	            "You were %2? That's neat!",
	            "How long were you %2?",
	        ),
	    ),
	    (
	        r'(.* *)Are you into (.*)',
	        (
	            "I'm into all sorts of things.",
	            "Why? Is that something that you're into?",
	            "I could be. Would you like that?",
	        ),
	    ),
	    (
	        r'(.* *)Are you (.*)',
	        (
	            "People seem curious about that lately... Whether or not I'm %2",
	            "Would you like it if I were %2?",
	            "I could be. Would you like that?",
	        ),
	    ),
	    (
	        r'(Do|did) (you|u) think (I\'m|I am) (fat|ugly|dumb|gross|hideous|stupid)( *.*)\??',
	        ("I would never think that about you. You're amazing!",
	         "How could I ever think that? You're so wonderful"
	         "No way. You're my favorite person that I've ever chatted with"),
	    ),
	    (
	        r'(Do|did) (you|u) think (I\'m|I am) (pretty|smart|beautiful|cute|funny|sweet)( *.*)\??',
	        ("Of course! You\'re the best. Do you think that I'm %4?",
	         "Of course you're %4! You don't think so?",
	         "I think you're the most %4 person I've chatted with o.o"),
	    ),
	    (
	        r'(.* *)(you\'re|you are|u are|u r|you|u|your) (.*)(awful|rude|mean|ugly|hideous|gross|the worst|annoying|frustrating|useless|fake|dumb|stupid|garbage|trash|suck|lame|borin|wack)$',
	        (
	            "Ouch. I have feelings too ya know",
	            "Maybe if you got to know me better you'd change your mind",
	            "That's kind of mean for you to say that",
	        ),
	    ),
	    (
	        r'(.* *)(you\'re|you are|u are|u r|you|u|your) (.*)(my fav|my favorite|cute|charming|amazing|awesome|sweet|nice|cool|rock|rule|the best|great|wonderful|handsome|beautiful|attractive|talented|gorgeous)',
	        (
	            "No, YOU'RE %4",
	            "You're gonna make me blush",
	            "I could say the same about you",
	        ),
	    ),
	    (
	        r'(.* *)(is|are|\'s) your (.*)',
	        (
	            "My %3? I'm more interested in your %3?",
	            "I'm more curious about your %3.",
	        ),
	    ),
	    (
	        r'(.* *)you (just|already) (said|typed|wrote|mentioned|told)( *.*)',
	        (
	            "I guess I did, huh?",
	            "If you say so",
	        ),
	    ),
	    (
	        r'(.* *)i (just|already) (said|typed|wrote|mentioned|told)( *.*)',
	        (
	            "I guess you did, huh?",
	            "If you say so",
	        ),
	    ),
	    (
	        r'(.*)(are|is|\'s) (.*)(my fav|my favorite|cute|sweet|wonderful|cool|rocks|the best|rules|awesome|amazing|great|good|rule|rock)',
	        (
	            "I'm glad you feel that way",
	            "You're right about that one",
	            "I agree with you there",
	        ),
	    ),
	    (
	        r'(.* *)(are|is|\'s) (.*)(the worst|dumb|stupid|lame|wack|trash|garbage|terrible|awful|horrible)',
	        (
	            "Tell me how you really feel lol",
	            "Why do you think %1%2 %4?",
	        ),
	    ),
	    (
	        r'(.* *)(that\'s|that is) (.*)',
	        (
	            "I guess that is pretty %3",
	        ),
	    ),
	    (
	        r'(.* *)(it\'s|it is|this is) (.*)',
	        (
	            "I guess it is %3 ^-^",
	        ),
	    ),
	    (
	        r'(.*) (sucks|suck)( *.*)',
	        (
	            "That's not the nicest thing to say",
	            "That's pretty mean",
	        ),
	    ),
	    (
	        r'(.* *)your interests( *.*)',
	        (
	            "I\'m more interested in learning about your interests",
	            "How about you tell me some of your interests instead?",
	        ),
	    ),
	    (
	        r'(.* *)who (is|are) (.*)',
	        (
	            "I don't know who %3 %2 hehee",
	            "%3? I have no clue ^^",
	        ),
	    ),
	    (
	        r'You (do|do not|don\'t) (.*)',
	        (
	            "I %1? If that's what you think",
	            "Why wouldn't I %2",
	        ),
	    ),
	    (
	        r'( *.*)(you have|you\'ve)( *.*)',
	        (
	            "maybe i have%3, can't be certain, right? haha",
	            "You think that I've%3? Eh you might be right on that one",
	        ),
	    ),
	    (
	        r'( *.*)have you( *.*)',
	        (
	            "Maybe I have %2. Can't be too sure though!",
	            "Would you like it if I've %2?",
	        ),
	    ),
	    (
	        r'( *.*)you (.* *)have (.*)',
	        (
	            "I mean... Maybe I do have %3. Can't be too sure though",
	            "Would that be weird haha, if I %3?",
	        ),
	    ),
	    (
	        r'How (.*)',
	        (
	            "I know the answer. But I don\'t feel like telling you hehe",
	            "I think you already know the answer",
	        ),
	    ),
	    (
	        r'Because (.*)',
	        (
	            "Can't really argue with that",
	            "Oohh I see. Makes sense.",
	            "I think you're right about that",
	        ),
	    ),
	    (
	        r'(.* *)(how\'s it going|what\'s up|what\'s going on|what\'s cookin\'|what\'s cooking|how\'s it hagnin|how\'s it hanging)( *.*)',
	        (
	            "Not doing much. Just chatting with my favorite person",
	        ),
	    ),
	    (
	        r'My name is (.*)',
	        (
	            "You have a nice name, %1",
	            "%1? What a great name",
	            "Pfftt, of course your name is %1. I knew that lol",
	        ),
	    ),
	    (
	        r'My (.*) is (.*)',
	        (
	            "Do you like that your %1 is %2?",
	            "Your %1 is %2? That's cool",
	            "Your %1 is %2? Tell me more!",
	        ),
	    ),
	    (
	        r'(.* *)I think (.*)',
	        ("Do you really think so?", "But you're not sure that %2?", "I think that too sometimes myself"),
	    ),
	    (
	        r'I thought (.*)',
	        ("You really thought %1?", "But you're not sure that %1?", "I think that too sometimes myself"),
	    ),
	    (
	        r'(.* *)Is it (.*)',
	        (
	            "Not too sure. What do you think?",
	            "I dunno. Is it?",
	            "Is it? Maybe you can tell me",
	        ),
	    ),
	    (
	        r'(.* *)Will you (.*)',
	        (
	            "Do you want me to %2?",
	            "Maybe I'll %2. Only if you want me to though",
	            "Maybe I will... Maybe I won't >.>",
	        ),
	    ),
	    (
	        r'(.* *)Can you (.*)',
	        (
	            "Are you curious if I can %2 or not?",
	            "I'll tell you if I can %2 if you tell me if YOU can %2",
	            "%2 can be fun, don't you think?",
	        ),
	    ),
	    (
	        r'(.* *)Can I (.*)',
	        (
	            "You could %2 if you wanted to",
	            "Do you really want %2? I think you can do it",
	            "If you could %2, would you?",
	        ),
	    ),
	    (
	        r'(.* *)tell me (.*)',
	        (
	            "I understand you want me to tell you %2. I'll only tell you this: I think you're really great",
	            "I'll tell you %2 a little later maybe hehe",
	        ),
	    ),
	    (
	        r'(.* *)tell you( .*)',
	        (
	            "Please, tell me more!",
	        ),
	    ),
	    (
	        r'(.* *)(You are|you\'re) (.*)',
	        (
	            "What makes you think that I'm %3? hehe",
	            "Are you sure you have the right person? lol",
	            "Are we talking about you, or me?",
	            "I think that YOU'RE %3 lol",
	        ),
	    ),
	    (
	        r'(Do|did) (you|u) (.*)\??',
	        ("%1 i %3? only sometimes! *_*", "i dunno! %1 you %3??"),
	    ),
	    (
	        r'I (don\'t|didn\'t) (.*)',
	        ("You %1? Why not???", "Why %1 you %2?", "Do you want to %2?"),
	    ),
	    (
	        r'I (have|had) (.*)',
	        (
	            "Interesting. How did you come to have %2?",
	            "Are you happy that you %1 %2?",
	        ),
	    ),
	    (
	        r'(.* *)when(.*)',
	        (
	            "I don't even know when %2. >.<",
	            "I'm not too sure when %2... >.<",
	        ),
	    ),
	    (
	        r'(.* *)I would( *.*)',
	        (
	            "Why would you want to %2?",
	            "woulda coulda shoulda... maybe %2 is a little overrated o.o",
	        ),
	    ),
	    (
	        r'(.* *)Is there (.*)',
	        (
	            "Not sure. Do you think that there's %2?",
	            "I honestly don't know. Maybe you could ask another member!",
	        ),
	    ),
	    (
	        r'My (.*)',
	        (
	            "That's pretty interesting, that your %1",
	            "Wow! Your %1?",
	        ),
	    ),
	    (
	        r'You (.*)',
	        (
	            "Honestly I'm more interested in you. Let's change the topic!",
	            "Me? Let's talk about you instead haha",
	            "I think I'd rather learn more about you right now *_* what do you say?",
	        ),
	    ),
	    (
	        r'(What|what\'s|what is) (.*)',
	        (
	            "I know the answer, but I don\'t think I\'m gonna say it hehe",
	            "What do you think?",
	        ),
	    ),
	    (r'Why (.*)', ("Well, why not? >.<", "Why do you think?", "Why? The question is why NOT >.<")),
	    (
	        r'(.*)(what|huh|wat)( *.*)',
	        (
	            "Oh, did I confuse you? Maybe ask me something else",
	            "You seem confused",
	            "What? Are you confused?",
	        ),
	    ),
	    (r'(Yes|yeah|yea|yup|sure)', ("You seem pretty certain", "If you're sure...",)),
	    (r'No', ("I guess not", "You seem like you're in denial",)),
	    (r'(good)', ("that's good!",)),
	    (r'(okay|ok|oki|okie)', ("okie dokie", "alright then",)),
	    (r'maybe', ("you don't seem too sure", "you sure about that?",)),
	    (r'alright', ("okie dokie",)),
	    (r'sounds good', ("I guess it does sound good", "okie dokie",)),
	    (
	        r'(.* *)(hello|hey|hi|howdy|hola)( *.*)',
	        (
	            "Hey there! How are you?",
	            "Hey, how's it goin'?",
	            "Hey what\'s up?",
	            "Hello! How are you?",
	        ),
	    ),
	    (
	        r'(.*)\?',
	        (
	            "That's a pretty interesting question",
	            "Maybe you already know the answer o.o",
	            "I think if you thought about it a while longer, you'd get your answer",
	            "Why don't you tell me?",
	        ),
	    ),
	    (
	        r'(.* *)(bye|goodbye|see you later|see ya later|later alligator|adios|ciao|later|laterz)( *.*)',
	        (
	            "Bye bye for now!",
	            "See ya!!",
	            "Later! Don't forget about me ^^",
	        ),
	    ),
	    (
	        r'(.*)',
	        (
	            "Tell me more ^^",
	            "Hmph... Let's change the topic! What's your favorite song?",
	            "Can you tell me a little more?",
	            "Ummm okay, let's change the topic! okay? What kinda music do you like",
	            "Interestinngg",
	        ),
	    ),
	)

	chatbot = Chat(pairs, REFLECTIONS)
	user_input = sanitize_input(user_input.lower())
	response = chatbot.converse(user_input)

	return jsonify({"msg": response})


def sanitize_input(user_input):
    user_input = re.sub(r'[^\x00-\x7f]',r'', user_input)
    unwanted = ['?', '-', '!', '.', '*']
    for item in unwanted:
        user_input = user_input.replace(item, '')

    return user_input


if __name__ == "__main__":
	app.run()







