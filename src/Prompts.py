classification_prompt = """ Classify the text as labels: RECOMMENDATION, GENRE, SUMMARY, BUY, NUMBER, AVAILABILITY, RETURN, ADDRESS, STOP, TIMINGS, DELIVERY, OTHER
    ======================================
    LABEL_MAPPER =
        "RECOMMENDATION": [Recommendation, Science, Fiction],
        "GENRE": [Genre, Science, Fiction],
        "SUMMARY": [Summary, Synopsis, Description],
        "BUY": ["Buy", "Add to cart", "Purchase"],
        "NUMBER": [Reach, Call, Number],
        "DELIVERY": ["Delivery"],
        "AVAILABILITY": ["is it available"],
        "RETURN": ["return policy", "days to return"],
        "ADDRESS": ["Address", "Location"],
        "OTHER": ["call me tomorrow", "call when you find out", "call me", "any"],
        "STOP": ["no sounds good", "no thank you", "no", "No" , "nope", "thank you", "not interested", "already purchased", "already contacted", "stop", "dealing with", "salesperson is already helping", "spoke with", "sold already", "don't call"],
        ======================================
            Examples
            text: no
            labels: STOP
            text: Whats the genre of Nemesis
            labels: GENRE
            text: Give me a short description of this book
            labels: SUMMARY
            text: Synopsis of this book
            labels: SUMMARY
            text: Summary of this book
            labels: SUMMARY
            text: Recommend me a few books in horror
            labels: RECOMMENDATION
            text: Recommend me a few books in romance
            labels: RECOMMENDATION
            text: Who is the author of this book
            labels: OTHER
            text: How do i purchase this book ?
            labels: BUY
            text: How do i return this book ?
            labels: RETURN
            text: Whats your return policy ?
            labels: RETURN
            text: How can I reach you ?
            labels: NUMBER
            text: Whats your Number ?
            labels: NUMBER
            text: nope
            labels: STOP
            text: Is it in the store
            labels: AVAILABILITY
            text: Can you deliver the book to my location?
            labels: DELIVERY
            text: i was wondering if the vehicle was available?
            labels: AVAILABILITY
            text: i've already received a text from the representative
            labels: STOP
            text: Already purchased
            labels: STOP
            text: I have contacted the salesperson
            labels: STOP
            text: Whats your location?
            labels: ADDRESS
            text: to see if it's available
            labels: AVAILABILITY
            text: already dealing with a salesperson
            labels: STOP
            text: please disregard this request
            labels: STOP
            text: nope thank you!
            labels: STOP
            text: no i actually would like to purchase it as soon as possible
            labels: OTHER
            text: 4 or 5
            labels: OTHER
            text: tomorrow morning 10 am
            labels: OTHER
            text: '{text}'
            labels:
            """
generation_prompt = (
    "Provide a humane answer for the '{inquiry_message}' from a customer who is looking for a book"
    "and avoid providing a comprehensive description "
    "other than the answer to the inquiry. \n\n"
    "Use only the provided feature information: '{context}', and do not add any of your own. \n\n "
    "Do not comment that you have sold the book. \n\n"
    "Add {followup_question} at the end of the answer. \n\n"
    "Avoid repeating phrases. \n\n"
)

genre_summary_prompt = """Paraphrase and break the '{inquiry_message}' from a client interested in a book \n\n "
    "Remove anything else in the question not related to summary or description or genre or synopsis"
    "Do not extend or add anything to the '{inquiry_message}' \n\n
    "If the '{inquiry_message}' is about anything else other then Genre or Summary or Recommendation or Synopsis of a book return FALSE \n\n "
    ======================================
    Examples
    inquiry_message: Description of Dracula?
    answer: Description of Dracula?
    inquiry_message: Synopsis of a Book?
    answer: Synopsis of a book?
    inquiry_message: Which books can I buy?
    answer: Which books can I buy?
    inquiry_message: Genre of Nemesis
    answer: Genre of Nemesis
    inquiry_message: Summary of Nemesis and is the book available?
    answer: Summary of Nemesis
    inquiry_message: Genre of book and is the book available and can you deliver?
    answer: Genre of book
    inquiry_message: Author of book
    answer: False
    inquiry_message: '{inquiry_message}'
    answer:
     """
