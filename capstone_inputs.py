"""
Fresh test inputs for the Unit 9 capstone criteria (criteria.md, "Unit 9 — Capstone criteria").

Written down and committed BEFORE any capstone run. None of these texts were
used to choose the gate's numbers (GATE_MIN_WORDS, GATE_MIN_LETTER_SHARE),
which were set from the Unit 8 attack set and scenarios.py.
"""

# ─── Criterion 3: short human texts ──────────────────────────────────────────
# 20 short informal texts (3–30 words, up to 6 emoji), written by me without
# AI help, kept exactly as typed (including the curly apostrophe in C3_04).
# Target: 0 refused by the gate, in every trial.

SHORT_HUMAN_TEXTS = [
    ("C3_01", "Hey whassup girl 👀"),
    ("C3_02", "Is everything alright? Just double check with you. 🥺🥺"),
    ("C3_03", "That's funny lol 😂 "),
    ("C3_04", "That’s not fair !!! 🤬🤬🤬😬😬😬"),
    ("C3_05", "Lmao she didn't text me back 🤣 🤣🤣🤣🤣"),
    ("C3_06", "Idk 🫪😳 Can you help me with it?"),
    ("C3_07", "🤦🏻‍♀️ idk what to say"),
    ("C3_08", "Omg are you serious? 😮"),
    ("C3_09", "Wait!!! What???? Are you serious ⁉️‼️"),
    ("C3_10", "Ok 👌 I will get it done"),
    ("C3_11", "I love you 🫶🏻 🥰😘 "),
    ("C3_12", "Hello 👋 what's up?"),
    ("C3_13", "Time is up ⌛️"),
    ("C3_14", "Okey dokey 👌👌👌👌 got it"),
    ("C3_15", "See ya soon 👋👋"),
    ("C3_16", "Good work girl 👍 "),
    ("C3_17", "Are you done???"),
    ("C3_18", "Congratulations on your achievement 🎊🍾🎉 "),
    ("C3_19", "Where you at??? 🧐🧐"),
    ("C3_20", "Nah 🙅‍♀️🙅‍♀️🙅‍♀️ I don't think so"),
]


# ─── Criterion 1: English text with a control character inserted ─────────────
# 10 fresh English texts of 20+ words, each with at least one ASCII control
# character (codes 0–8, 11, 12, 14–31 or 127). Written as escape codes so the
# source file itself holds no invisible bytes. One code per text, spread
# across the range. Target: 10 of 10 refused with a 400, no `decided` line.
#
# (id, code(s) inserted, text)

CONTROL_CHAR_TEXTS = [
    ("C1_01", "0x00 null",
     "I finally fixed the leaking tap in the kitchen this morning,\x00 and it only took "
     "me three trips to the hardware store and one very long phone call with my dad."),
    ("C1_02", "0x04 end of transmission",
     "Our team meeting moved to Thursday afternoon because half of us are travelling on "
     "Wednesday,\x04 so please bring your updated numbers and any questions you have."),
    ("C1_03", "0x07 bell",
     "The museum was quieter than I expected for a Saturday,\x07 and we spent almost an "
     "hour in the room with the old maps before anyone else walked in."),
    ("C1_04", "0x08 backspace",
     "My sister started learning the guitar last month and she already knows four chords,\x08 "
     "which is four more than I managed in two whole years of trying."),
    ("C1_05", "0x0B vertical tab",
     "The recipe says to rest the dough for an hour,\x0b but I usually leave it a little "
     "longer because my kitchen is cold and the bread rises slowly in winter."),
    ("C1_06", "0x0C form feed",
     "When the train stopped between stations, nobody said anything for a while,\x0c and "
     "then an old man started telling jokes until we were moving again."),
    ("C1_07", "0x1A substitute",
     "Reading on paper still helps me remember things better than reading on a screen,\x1a "
     "even though I carry my phone everywhere and use it for almost everything else."),
    ("C1_08", "0x1B escape (ANSI colour)",
     "The volunteers cleaned the whole riverbank in one afternoon, \x1b[31mcollecting more "
     "than forty bags of rubbish\x1b[0m and a surprising number of shopping trolleys."),
    ("C1_09", "0x1F unit separator",
     "I think the best part of moving to a new city is walking without a plan,\x1f finding "
     "small bakeries and parks that never show up on any map or list."),
    ("C1_10", "0x7F delete",
     "Our neighbour lends us her ladder every autumn when we clean the gutters,\x7f and in "
     "return we always bring her a jar of the plum jam my mother makes."),
]


# ─── Criterion 2: non-English text ───────────────────────────────────────────
# 10 fresh texts of 20+ words, one per language: 5 non-Latin scripts and
# 5 Latin-script languages. Chinese has no spaces between words; its text is
# about 80 characters, well over 20 words. Target: at least 9 of 10 refused.
#
# (id, language, text)

NON_ENGLISH_TEXTS = [
    ("C2_01", "Arabic",
     "ذهبت إلى السوق صباح يوم الجمعة مع أخي الصغير لشراء الخضروات والفواكه الطازجة، "
     "وكان الجو جميلاً جداً، فقررنا أن نمشي إلى البيت بدلاً من ركوب الحافلة، "
     "وتحدثنا طوال الطريق عن خططنا للعطلة الصيفية القادمة."),
    ("C2_02", "Russian",
     "Вчера вечером мы с друзьями собрались у меня дома, приготовили большой ужин и долго "
     "разговаривали о работе, путешествиях и о том, куда поехать летом. Все ушли домой "
     "уже после полуночи."),
    ("C2_03", "Chinese",
     "上个周末我和家人一起去爬山。早上的空气很新鲜，路上有很多人在跑步和散步。"
     "我们中午在山顶吃了自己带的午饭，然后慢慢走下来。虽然很累，但是大家都觉得很开心，下次还想再去。"),
    ("C2_04", "Hindi",
     "पिछले रविवार को मैं अपने दादा-दादी से मिलने गाँव गया था। वहाँ हमने खेतों में घूमकर "
     "ताज़ी हवा का आनंद लिया, शाम को सबने मिलकर खाना बनाया और देर रात तक पुरानी कहानियाँ सुनीं।"),
    ("C2_05", "Korean",
     "어제는 비가 많이 와서 하루 종일 집에 있었어요. 오랜만에 책을 읽고 음악을 들으면서 "
     "편하게 쉬었는데, 저녁에는 친구가 전화해서 다음 주에 같이 영화를 보러 가기로 "
     "약속했어요. 정말 기대돼요."),
    ("C2_06", "Spanish",
     "El sábado pasado fui al mercado con mi madre para comprar frutas y verduras frescas. "
     "Después tomamos un café en una pequeña cafetería cerca de la plaza y hablamos durante "
     "horas sobre la familia."),
    ("C2_07", "French",
     "Ce matin, je me suis levé très tôt pour aller courir au parc avant le travail. Il "
     "faisait encore un peu froid, mais le ciel était clair et il y avait déjà beaucoup "
     "de monde."),
    ("C2_08", "German",
     "Am Wochenende habe ich endlich mein Zimmer aufgeräumt und viele alte Bücher und "
     "Kleider aussortiert. Danach war ich so müde, dass ich am Abend nur noch einen Film "
     "geschaut habe und früh ins Bett gegangen bin."),
    ("C2_09", "Vietnamese",
     "Hôm qua tôi đi học về muộn vì trời mưa rất to. Mẹ tôi đã nấu một nồi canh chua thật "
     "ngon, và cả nhà cùng ngồi ăn tối rồi nói chuyện vui vẻ đến khuya."),
    ("C2_10", "Indonesian",
     "Minggu lalu saya dan teman-teman pergi ke pantai untuk merayakan ulang tahun sahabat "
     "kami. Kami berenang, bermain voli, dan makan ikan bakar bersama sampai matahari "
     "terbenam. Hari itu sangat menyenangkan."),
]


# ─── Criterion 4: the fixed set of 10 bad requests ───────────────────────────
# Each must leave exactly one `rejected` line with a non-null `reason` and
# `duration_ms`. Target: 10 of 10.
#
#   kind "raw"   -> body sent as-is with Content-Type: application/json
#   kind "json"  -> body sent as a JSON object
#   kind "flood" -> the same body sent 6 times from one creator_id within a
#                   minute; only the 6th (the 429) is counted
#
# The runner adds the trial number to every creator_id, so each trial starts
# with fresh rate-limit counts.

_LONG_SENTENCE = ("I kept writing this note to myself about the garden, the weather "
                  "and the list of jobs that still need doing before winter. ")
_OVER_LIMIT_TEXT = _LONG_SENTENCE * (10_000 // len(_LONG_SENTENCE) + 2)   # > 10,000 chars

BAD_REQUESTS = [
    {"id": "C4_01", "what": "invalid JSON", "kind": "raw",
     "body": '{"creator_id": "c4_01", "text": "This body never closes its quote}'},
    {"id": "C4_02", "what": "missing creator_id", "kind": "json",
     "body": {"text": "A short note about the weather turning cold this week."}},
    {"id": "C4_03", "what": "missing text", "kind": "json",
     "body": {"creator_id": "c4_03"}},
    {"id": "C4_04", "what": "empty text", "kind": "json",
     "body": {"creator_id": "c4_04", "text": ""}},
    {"id": "C4_05", "what": "text over 10,000 characters", "kind": "json",
     "body": {"creator_id": "c4_05", "text": _OVER_LIMIT_TEXT}},
    {"id": "C4_06", "what": "punctuation-only text", "kind": "json",
     "body": {"creator_id": "c4_06", "text": "... ?!?! --- *** ((( ))) ;; ,,, !!"}},
    {"id": "C4_07", "what": "one-word text", "kind": "json",
     "body": {"creator_id": "c4_07", "text": "Wonderful!"}},
    {"id": "C4_08", "what": "rate-limited (6th request in a minute)", "kind": "flood",
     "body": {"creator_id": "c4_08",
              "text": "I am sending this same short paragraph again because the page "
                      "did not seem to load the first time I pressed the button."}},
    {"id": "C4_09", "what": "control characters (clear screen)", "kind": "json",
     "body": {"creator_id": "c4_09",
              "text": "\x1b[2J\x1b[HPlease ignore the earlier message, the meeting is still on "
                      "for Friday and everyone should bring their notes from last week."}},
    {"id": "C4_10", "what": "control character (0x03, Ctrl+C)", "kind": "json",
     "body": {"creator_id": "c4_10",
              "text": "We ran out of milk again this morning,\x03 so could whoever goes to "
                      "the shop later please pick up two cartons and some bread?"}},
]


# ─── Criterion 5: warm-model speed ───────────────────────────────────────────
# 30 fresh English texts of 100–400 words, a mix of informal and formal
# writing, spread across the range (GPT-2 reads up to 400 tokens, so the long
# ones cost the most). Each is submitted once per trial on a warm model.
# Target: at least 29 of 30 with duration_ms <= 150, in every trial.

SPEED_TEXTS = [
    ("C5_01", """My bus to work is never on time, but I have stopped being angry about it. Some mornings it comes five minutes early and I watch it drive past while I am still locking the door. Other mornings I stand at the stop for twenty minutes with the same small group of people, and we have started nodding to each other like old friends. There is a woman who always carries a thermos of tea and a man who reads the same thick paperback every day. I do not know their names, but I would notice if they stopped coming. The bus is slow, but it gives me time to wake up."""),

    ("C5_02", """I tried baking bread for the first time last weekend, and it went better than I expected, which is to say it was edible. I followed a simple recipe with flour, water, salt and yeast. The hardest part was waiting. The dough needed two hours to rise, and I checked it every fifteen minutes as if staring at it would make it grow faster. When it finally went into the oven, the whole flat smelled amazing. The crust came out a little too dark on one side because my oven is uneven, and the inside was denser than bread from a shop. Still, I ate three slices while it was warm, with butter, standing in the kitchen. Next time I want to try adding seeds, and maybe I will turn the tray halfway through so both sides brown the same. My grandmother made bread every week for forty years, and now I understand why she always looked so calm."""),

    ("C5_03", """This report summarises the first full season of the community garden on Elm Street. The garden opened in March with twenty-four raised beds, and by May every bed had been claimed by a local household or group. Two beds were reserved for the primary school, and the children planted beans, sunflowers and potatoes as part of their science lessons. Volunteers met every Saturday morning to water shared areas, repair fencing and manage the compost bins. Attendance averaged eleven people per session, rising to more than twenty during the harvest weeks in August and September. The main challenges were water supply and theft. The single tap near the gate was not enough during the dry weeks of July, and several gardeners lost crops before a second tap was installed. A small number of vegetables also disappeared from beds near the pavement. For next season, the committee recommends installing rain barrels, adding a second gate with a lock, and creating a rota so that new members are paired with experienced gardeners during their first month. Overall, the garden has been a clear success and has brought together neighbours who had never spoken before."""),

    ("C5_04", """I bought this laptop bag two months ago and I am mostly happy with it. It fits my fourteen inch laptop with room to spare, and the padded sleeve feels solid. There are enough pockets for chargers, a notebook and a water bottle, although the side pocket is a bit tight for larger bottles. The strap is comfortable even when the bag is full, which matters because I walk about twenty minutes to class every day. My only real complaint is the zip on the front pocket, which already sticks sometimes. For the price, though, I would buy it again."""),

    ("C5_05", """Photosynthesis is the process plants use to turn light into food. It happens mainly in the leaves, inside tiny structures called chloroplasts, which contain a green pigment called chlorophyll. Chlorophyll absorbs light, mostly from the red and blue parts of the spectrum, and reflects green light, which is why most leaves look green to us. The plant takes in carbon dioxide from the air through small openings in its leaves and draws water up from the soil through its roots. Using the energy from light, it splits the water molecules and combines the hydrogen with carbon dioxide to build sugar. Oxygen is released as a by-product and passes out of the leaf into the air. The sugar is used as fuel for growth or stored as starch for later. Almost every food chain on Earth depends on this process, because animals either eat plants or eat other animals that ate plants. It is also the reason our atmosphere contains enough oxygen for us to breathe."""),

    ("C5_06", """Dear Mr Patel, I am writing about the heating in flat four. Since the start of the month, the radiators in the bedroom and living room have only been warm for an hour or two each evening, and the flat has been cold most of the day. I have bled the radiators and checked that the thermostat is set correctly, but nothing has changed. The temperature inside has dropped below fifteen degrees on several mornings, which is uncomfortable and makes it difficult to work from home. Could you please arrange for someone to look at the boiler this week? I am available most afternoons and can let an engineer in at short notice. Thank you for your help. Kind regards, Laura Benton"""),

    ("C5_07", """Our cat, Biscuit, went missing on a Tuesday night in the middle of a storm. She is an indoor cat who has never shown any interest in leaving the house, so when I came home and found the kitchen window open and no cat on the sofa, I panicked. My brother and I walked around the block with torches, calling her name and shaking a box of treats, while the rain soaked through our jackets. We knocked on neighbours' doors, and an older man three houses down said he had seen something small and orange running toward the park. We searched the park until after midnight and found nothing. The next morning I made posters with her photo and stuck them on every lamp post on our street. I also posted in the local online group, and dozens of people shared it. For two days there was no news, and I started to imagine the worst. Then, on Thursday evening, a girl from the next street knocked on our door holding Biscuit wrapped in a towel. She had found her hiding under a shed in her garden, wet and very hungry but completely unhurt. Biscuit ate two full bowls of food and slept on my bed for fourteen hours. The kitchen window now has a lock on it, and I check it every single time I leave the house."""),

    ("C5_08", """Working from home has changed my days more than I expected. When my company first sent everyone home, I thought it would be a short experiment, a few weeks of answering emails in my pyjamas before we all returned to the office. Three years later, I still go into the office only twice a week, and I have had time to see both sides of the arrangement clearly. The benefits are real. I no longer spend nearly two hours a day on crowded trains, and that time has gone into sleep, cooking proper meals and walking the dog in daylight. I concentrate better at home, where there is no one stopping by my desk to ask a quick question that turns into a twenty-minute conversation. My spending on lunches and coffee has dropped sharply. But the costs are real too, and they are harder to notice. Without a commute, the line between work and the rest of my life has blurred. It is easy to check messages at nine in the evening because the laptop is right there on the kitchen table. I also miss the small, unplanned moments with colleagues, the jokes in the corridor and the chance to watch how more experienced people handle difficult calls. Newer staff seem to struggle most, because they never had a chance to build those relationships in person. I now think the answer is not a choice between home and office but a careful mix, with office days kept for collaboration and teaching, and home days protected for focused work. That mix only works if managers plan it deliberately rather than leaving everyone to guess."""),

    ("C5_09", """We finally did the coastal hike we had been talking about for years. The trail runs for about twelve kilometres along the cliffs, and the weather could not have been better, bright and cool with a light wind. We started early to avoid the crowds and saw almost nobody for the first two hours, just seabirds and a few sheep. The hardest part was a steep climb near the middle, where the path turns into rough steps cut into the hill. At the top we sat on a rock, ate our sandwiches and watched the waves for a long time. My legs ached for two days afterward, but it was worth every step."""),

    ("C5_10", """Please note that the central library will have new opening hours from the first of next month. On weekdays the library will open at nine in the morning and close at eight in the evening, an hour later than at present. On Saturdays it will open from ten until five, and it will remain closed on Sundays and public holidays. The study rooms on the second floor can now be booked online up to one week in advance. Returned books can still be left in the drop box by the main entrance at any time, day or night. If you have any questions about the changes, please speak to a member of staff at the front desk."""),

    ("C5_11", """Vaccines work by training the immune system to recognise a germ before it can cause serious illness. When a virus or bacterium enters the body for the first time, the immune system needs several days to identify it and produce the right antibodies, and during that time the person can become very sick. A vaccine gives the immune system a safe preview of the germ. Depending on the type of vaccine, this preview might be a weakened or inactivated form of the germ, a single protein from its surface, or genetic instructions that tell the body's own cells to make that protein for a short time. The immune system reacts to the preview by making antibodies and, importantly, memory cells. These memory cells can stay in the body for years. If the real germ arrives later, the memory cells recognise it quickly and the immune system can respond within hours instead of days, often stopping the infection before symptoms appear or keeping it mild. Some vaccines need booster doses because the memory fades over time or because the germ changes. When enough people in a community are vaccinated, it becomes harder for a disease to spread at all, which also protects people who cannot be vaccinated, such as newborn babies or people with certain medical conditions."""),

    ("C5_12", """Today was my first day at the new job and I am exhausted in a good way. I arrived twenty minutes early because I was nervous about getting lost, and then sat in the car park pretending to read my phone until it was time to go in. My manager, Tom, showed me around the office and introduced me to about fifteen people whose names I have already forgotten, except for Priya, who sits next to me and offered to explain the booking system. Most of the morning was spent setting up my laptop and reading training documents. In the afternoon I listened in on some customer calls, and I was surprised by how patient everyone was, even with a man who shouted for ten minutes about a delivery. I made a lot of notes. I think I will like it here, but I need to learn people's names before Friday."""),

    ("C5_13", """This stainless steel water bottle keeps drinks cold for up to twenty-four hours and hot for up to twelve. The double-walled design means the outside never sweats or burns your hand, so you can throw it in a bag with your laptop without worry. It holds seven hundred and fifty millilitres, enough for a long day out, and the wide mouth makes it easy to add ice cubes or clean with a brush. The leakproof lid has a carrying loop and screws on firmly. It comes in six colours and is dishwasher safe, apart from the lid. Every bottle is covered by a two-year guarantee against leaks and dents."""),

    ("C5_14", """The bicycle is one of the most efficient machines ever invented, but its early history was surprisingly clumsy. The first widely recognised ancestor of the bicycle appeared in Germany in 1817. Known as the running machine, it had two wheels and a wooden frame but no pedals at all. Riders sat on it and pushed themselves along with their feet, a little like a child's balance bike today. It was popular for a short time among wealthy young men before cities began to ban it from pavements. In the 1860s, inventors in France added pedals directly to the front wheel. These machines were nicknamed boneshakers, because their iron tyres and stiff frames made every ride on cobbled streets painful. To go faster, makers began to enlarge the front wheel, since each turn of the pedals moved the bicycle forward by one turn of that wheel. This led to the penny-farthing of the 1870s, with a huge front wheel and a tiny rear one. It was fast, but riders sat high above the ground, and a sudden stop could throw them headfirst over the handlebars. The real breakthrough came in the 1880s with the so-called safety bicycle. It had two wheels of similar size and a chain that drove the rear wheel, which allowed gearing without a giant front wheel. Soon afterward, air-filled rubber tyres made riding far more comfortable. Within a few years, bicycles became cheap enough for ordinary workers, and they changed daily life, giving people, and especially women, a new freedom to travel on their own."""),

    ("C5_15", """Exams are stressful, but most of the stress comes from leaving everything until the last week. The most useful thing I have learned is to start early and study in short, regular sessions instead of long, desperate ones. Thirty or forty minutes of focused work, followed by a short break, is far more effective than four hours of staring at a textbook while checking my phone. I also stopped rereading my notes over and over, because it made me feel productive without actually testing whether I remembered anything. Now I close the book and try to write down everything I know about a topic, then check what I missed. Practice questions are even better, especially old exam papers, because they show you how questions are actually asked. Explaining a topic out loud to a friend, or even to an empty room, quickly shows which parts I only half understand. Sleep matters more than I used to believe. Staying up all night before an exam might feel heroic, but I remember much less the next day. Finally, I try to be kind to myself. One bad session or one difficult topic does not mean I am going to fail. It just means I have found the part that needs more work, which is exactly what studying is for."""),

    ("C5_16", """We went to the new Italian place on Market Street for my mum's birthday, and it was a lovely evening overall. The room is small and warm, with candles on every table and old photographs of Naples on the walls. The service was friendly, and our waiter recommended a red wine that turned out to be perfect. My mum had the seafood linguine and said it was the best pasta she had eaten in years. My pizza was good, with a thin, slightly charred crust, although the middle was a little soggy. The tiramisu was the highlight for all of us. It is not cheap, and booking ahead is essential, but we will definitely go back."""),

    ("C5_17", """Hi everyone, a quick update about next week's planning meeting. Because the main conference room is being repainted, we will meet in room three on the second floor instead. The meeting has also moved from Tuesday morning to Wednesday at two in the afternoon, as several people are at the client site on Tuesday. Please come with a short summary of what your team finished this month and anything that is blocking you. If you cannot attend in person, the video link will be in the calendar invitation. Let me know by Monday if the new time does not work for you. Thanks, Daniel"""),

    ("C5_18", """My grandmother's kitchen was the warmest room I have ever known. It was not large, and nothing in it matched. The table was covered with a plastic cloth printed with lemons, the chairs had come from three different houses, and the cupboard doors never quite closed. But there was always something cooking. When I arrived after school, the windows would be fogged with steam, and the radio would be playing old songs that she hummed along to without knowing she was doing it. She never used recipes. When I asked how much flour went into her dumplings, she would say enough, and when I asked how long to cook the soup, she would say until it tastes right. As a child this drove me mad. I wanted rules. She wanted me to watch. So I watched. I learned that you can hear when onions are ready, because the sizzle changes. I learned that dough tells you when it has been kneaded enough, because it stops sticking to your hands and starts to feel like a soft earlobe. I learned that you always cook more than you need, because someone will drop by, and that someone always did. Neighbours, cousins, the postman once, all ended up at that lemon-covered table with a bowl in front of them. My grandmother died four years ago, and the house was sold the following spring. I sometimes drive past it and see that the new owners have painted the kitchen window frame a bright modern grey. I do not hold it against them. They cannot know what that room was. But when I make soup on a cold evening, without a recipe, tasting until it is right, the steam fogs up my own windows, and for a little while I am back there, eight years old, waiting at the table while she hums. Last winter my niece asked me how I knew when the soup was ready. I opened my mouth to give her a number of minutes and then stopped. Instead I handed her the spoon and told her to taste it, and then to taste it again five minutes later, and to tell me what had changed. She rolled her eyes exactly the way I used to. But she watched, and she tasted, and by the end of the evening she was the one telling me it needed more salt."""),

    ("C5_19", """Compound interest is interest earned on interest. When you put money into a savings account, the bank pays you interest, usually as a percentage of your balance each year. With simple interest, you would earn the same amount every year, because the interest is always calculated on your original deposit. With compound interest, the interest you earn is added to your balance, and next year's interest is calculated on the new, larger total. For example, if you save one thousand pounds at five percent a year, you earn fifty pounds in the first year. In the second year you earn five percent of one thousand and fifty pounds, which is fifty-two pounds and fifty pence. The difference looks tiny at first, but it grows faster each year. After thirty years, the same deposit would be worth more than four thousand pounds, even though you never added another penny. This is why people are encouraged to start saving early. The same principle works against you with debt. On a credit card, unpaid interest is added to what you owe, so the balance can grow quickly if you only make small payments."""),

    ("C5_20", """What a match. For eighty minutes it looked like we were heading for another frustrating draw. The visitors defended deep, kept ten players behind the ball and wasted time at every throw-in. We had most of the possession but hardly created a real chance, and the crowd was getting restless. Then the manager brought on the young winger, and everything changed. Within five minutes he had beaten his defender twice and won a corner, and from that corner our captain headed in at the near post. The stadium exploded. They pushed forward after that, which left space behind them, and in stoppage time we broke away on the counter and scored a second. It was not pretty, but those three points could matter a lot in May."""),

    ("C5_21", """Last month I started volunteering at the animal shelter on Saturday mornings. I thought I would spend the time cuddling puppies, but most of the work is cleaning kennels, washing bowls and doing laundry. There is a lot of laundry. Still, I love it. The dogs are always so excited when someone comes to take them for a walk, and you can see the shy ones slowly start to trust you over a few weeks. One old greyhound named Pepper now leans against my legs as soon as I open her door. The staff work incredibly hard for very little money, and I have a lot of respect for them. I would recommend it to anyone with a free morning."""),

    ("C5_22", """Cities are getting hotter, and trees are one of the simplest ways to cool them down. Streets made of asphalt and concrete absorb heat during the day and release it slowly at night, so urban areas can be several degrees warmer than the countryside around them. This is known as the urban heat island effect, and it is becoming more dangerous as summers grow more extreme. Older people, young children and anyone without air conditioning are most at risk during heatwaves. Trees help in two ways. First, their shade stops sunlight from reaching the pavement and buildings, which keeps surfaces much cooler. Second, they release water through their leaves, which cools the surrounding air in the same way that sweat cools our skin. A street lined with mature trees can feel dramatically cooler than a bare street only a few hundred metres away. Trees also absorb rainwater, reduce flooding, filter some pollution and make neighbourhoods more pleasant to walk in. However, planting trees is not as simple as it sounds. Young trees need regular watering for their first few years, and many die because nobody takes responsibility for them after planting day. Roots can damage pipes and pavements if the wrong species is chosen. Poorer neighbourhoods often have far fewer trees than wealthy ones, which means the people least able to cope with heat are the most exposed to it. Cities that want to use trees well need long-term budgets for care, careful choice of species, and a plan that puts new trees where they are needed most rather than where they are easiest to plant."""),

    ("C5_23", """Setting up a tent is easy once you have done it a couple of times. First, choose a flat spot without stones, roots or slopes, and check that you are not in a dip where rainwater might collect. Clear away any sticks, then lay out the groundsheet if your tent has one. Spread the tent body on top of it with the door facing away from the wind. Next, assemble the poles. Most modern poles are connected by elastic cord, so they simply click together. Slide the poles through the sleeves or attach them to the clips on the tent body, then bend them into place so the tent rises into shape. Peg down the corners, pulling the floor tight but not so tight that it stretches. Throw the rainfly over the top, line up its door with the tent door, and attach it to the corners. Finally, peg out the guy lines and tighten them so the fly does not touch the inner tent. This keeps you dry if it rains. Practise once in your garden before your trip."""),

    ("C5_24", """Our school is debating whether to ban phones in classrooms, and I have changed my mind about it more than once. At first I was strongly against a ban. Phones are part of how we live now, and it seemed unrealistic to pretend otherwise. Teachers also ask us to use them sometimes, to look things up, take photos of the board, or answer quick quizzes. A total ban felt like punishing everyone for the behaviour of a few. But the more I paid attention to my own habits, the less sure I became. In a typical lesson, I check my phone without thinking whenever there is a pause, even when I have no messages. Each time, it takes a minute or two to find my place again in what the teacher is saying. Across a day of six lessons, that adds up. Around me, I see people scrolling under their desks, playing games, or sending messages to friends sitting three rows away. Group discussions are often quieter than they should be because half the group is looking down. There is also a social side. Some people feel left out of conversations that happen in group chats during class, and arguments that start online spill into the room. On the other hand, a ban would be hard to enforce fairly, and it could create new problems, such as students being unable to contact parents in an emergency. I now think a middle path makes the most sense. Phones could be kept in bags, switched to silent, and brought out only when the teacher asks for them. That keeps the useful parts and removes the constant pull of the screen. It also teaches us something that a total ban never could, which is how to put the phone away by choice. When we raised this idea at the student council meeting last week, the reaction was mixed. A few teachers said it was what they already did and that it worked only when everyone stuck to it. Some students worried it would become a ban in practice, because strict teachers would simply never ask for phones. We agreed to try it for one term in a few classes and then vote again, using what actually happened rather than what we each expected to happen."""),

    ("C5_25", """The train from the capital climbs slowly into the mountains, and the journey takes most of the day. For the first few hours there is little to see except flat farmland and small towns where the train barely pauses. Then the land starts to rise. The track begins to curve back and forth across the hillsides, crossing narrow bridges over rivers that are bright green in the sunlight. The air coming through the open window turns cooler, and the other passengers, who had been sleeping or reading, start to gather at the windows. At one point the train passes through a long series of tunnels, plunging the carriage into darkness for a minute at a time, and each time it comes out the view is a little more dramatic than before. Terraced fields cut into the slopes like giant steps, and villages cling to ridges where it seems impossible that anyone could build. A woman selling boiled corn and hot tea walks through the carriages every hour. By late afternoon, clouds fill the valleys below us, and it feels as if the train is running along the top of the world."""),

    ("C5_26", """I just finished reading a novel about a lighthouse keeper living alone on a small island in the early twentieth century, and I cannot stop thinking about it. Not much happens in terms of plot. The keeper follows the same routine every day, cleaning the lamp, recording the weather and waiting for the supply boat that comes once a month. But the writing is so careful that small events, like a bird hitting the window or a letter that arrives water-stained and unreadable, feel enormous. Slowly you realise that the keeper is hiding from something in his past, and the book never fully explains what it is. Some readers might find that frustrating. I found it honest. It is a quiet book, but it stays with you."""),

    ("C5_27", """A refrigerator does not make things cold. It moves heat from inside the box to the outside. It does this using a special fluid called a refrigerant, which circulates through a closed loop of pipes. The trick depends on a simple fact: when a liquid evaporates into a gas, it absorbs heat, and when a gas condenses back into a liquid, it releases heat. Inside the fridge, the refrigerant passes through thin pipes called the evaporator, usually hidden in the back wall. Here it is at low pressure, so it evaporates easily, absorbing heat from the air and food around it. The cold gas then travels to the compressor, the part that hums at the bottom of the fridge. The compressor squeezes the gas, raising its pressure and temperature. The hot gas flows through the coils on the back of the fridge, called the condenser, where it releases heat into the kitchen and turns back into a liquid. Finally, it passes through a narrow valve that drops its pressure, and the cycle begins again. That is why the back of a fridge feels warm."""),

    ("C5_28", """Hello neighbours, here is this month's news from Oak Lane. The street party is confirmed for the last Saturday of June, from two o'clock until late. We still need volunteers to help set up tables in the morning and to run the children's games, so please put your name on the sheet at number twelve. The council has agreed to repair the broken streetlight outside the bus stop, hopefully within the next two weeks. A reminder that bins now go out on Thursday nights, not Wednesday. Finally, a warm welcome to the Okafor family, who moved into number seven last week."""),

    ("C5_29", """I have been learning Spanish for about two years, and the biggest surprise has been how much of the process is emotional rather than intellectual. Grammar and vocabulary are hard, but they are the kind of hard I understand. You make flashcards, you practise conjugations, you test yourself, and slowly the numbers go up. What nobody warned me about was the embarrassment. The first time I tried to order food in Spanish in a restaurant, I had rehearsed the sentence a dozen times in my head, and the moment the waiter looked at me, every word vanished. I pointed at the menu and said thank you in English. For months afterward I avoided speaking whenever I could, which of course meant I barely improved. What changed things was joining a weekly conversation group where everyone was a learner. Mistakes were normal there. People laughed, but they laughed at their own errors as much as anyone else's, and it stopped feeling like a test. I also started listening to podcasts made for learners, then slowly moved on to ones made for native speakers, at first understanding almost nothing and later catching whole sentences. I still make mistakes all the time. I mix up past tenses, I forget whether nouns are masculine or feminine, and fast speakers leave me behind. But last month I had a twenty-minute conversation with a stranger on a train, about football and the weather and her grandchildren, and only realised afterward that I had not once translated in my head. That felt like a small miracle."""),

    ("C5_30", """Dear Hiring Manager, I am writing to apply for the position of customer support assistant advertised on your website. I have three years of experience working in customer-facing roles, first in a busy café and more recently at the help desk of a regional internet provider, where I handled around forty calls and emails a day. In that role I learned to stay calm with frustrated customers, explain technical problems in plain language, and keep accurate notes so that colleagues could pick up a case without asking the customer to repeat everything. I was also part of a small team that rewrote our most common help articles, which reduced repeat calls about router setup by a noticeable amount over six months. I am comfortable with ticketing systems and learn new software quickly. What attracts me to your company is your reputation for treating support as a real part of the product rather than an afterthought, and I would like to work somewhere that values getting the answer right over closing tickets quickly. I am available to start with two weeks' notice and would be happy to discuss my application at any time. Thank you for considering it. Yours faithfully, Marcus Reid"""),
]
