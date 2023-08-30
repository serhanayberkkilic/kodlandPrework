from flaskApp.backend.config import app,db,login_manager
from flaskApp.backend.models.questionModel import Question
from flaskApp.backend.models.userModel import User
from flaskApp.backend.models.quizModel import Quiz
from flaskApp.backend.models.userAnswerModel import UserAnswer
from flask import render_template,request,redirect,url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import requests
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    return render_template('index.html')


with app.app_context():
    db.drop_all()
    db.create_all()

    quiz1 = Quiz(
        name="Python'da AI Geliştirme Sınavı"
    )

    quiz2 = Quiz(
        name="Bilgisayar Görüşü Sınavı"
    )

    quiz3 = Quiz(
        name="NLP (Nöro-Dilbilim) Sınavı"
    )

    quiz4 = Quiz(
        name="Python Uygulamalarında AI Modelleri Sınavı"
    )

    db.session.add_all([quiz1, quiz2, quiz3, quiz4])

    q1 = Question(
        question_text="Bir makine öğrenimi projesine başlamadan önce, veri ön işleme neden önemlidir?",
        quiz_id=1, 
        option1="Veri modelleme işlemleri daha hızlı gerçekleştirilir.",
        option2="Verileri daha hızlı bir şekilde toplamak için gereklidir.",
        option3="Verilerin doğruluğunu artırır ve modelin daha iyi performans göstermesini sağlar.",
        option4="Veri ön işleme, projenin sonuçlarına hiçbir etki yapmaz.",
        correct_option=3 
    )

    q2 = Question(
        question_text="Bir sinir ağı (neural network) eğitimi sırasında ikincil eksen dönüşümünün (data augmentation) temel amacı nedir?",
        quiz_id=1,
        option1="Verilerin daha fazla özellikle zenginleştirilmesi.",
        option2="Veri boyutunu azaltmak.",
        option3="Overfitting'i (aşırı uydurma) önlemek ve modelin genelleme yapabilmesini sağlamak.",
        option4="Verilerin doğruluğunu artırmak için kullanılır.",
        correct_option=3
    )


    db.session.add_all([q1, q2])
    
    user1 = User(
        username="kullanici1",
        password="parola1"
    )

    user2 = User(
        username="kullanici2",
        password="parola2"
    )

    db.session.add_all([user1, user2])


    user_1_answer1 = UserAnswer(
        user_id=1,
        quiz_id=1,
        question_id=1,
        userOption=3
    )

    user_1_answer2 = UserAnswer(
        user_id=1,
        quiz_id=1,
        question_id=2,
        userOption=2
    )

    user_2_answer1 = UserAnswer(
        user_id=2,
        quiz_id=1,
        question_id=1,
        userOption=1
    )

    user_2_answer2 = UserAnswer(
        user_id=2,
        quiz_id=1,
        question_id=2,
        userOption=1
    )


    db.session.add_all([user_1_answer1, user_1_answer2, user_2_answer1, user_2_answer2])

    db.session.commit()




@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            try:
                username = request.form['username']
                password = request.form['password']


                # Kullanıcıyı veritabanına ekleyin
                user = User(username=username, password=password)

                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                return redirect(url_for('register_failed')) # Kullanıcı adı zaten varsa kayıt başarısız olur ileride değiştirilecek


            return redirect(url_for('register_successful'))
        return render_template('register.html')

    except :
        return redirect(url_for('register_failed'))


@app.route('/register_successful', methods=['GET'])
def register_successful():
    return render_template('register_successful.html')

@app.route('/register_failed', methods=['GET'])
def register_failed():
    return render_template('register_failed.html')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username,password=password).first()

        if user:

            if username==user.username and password==user.password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login_failed'))
        else:
            return redirect(url_for('login_failed'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user_answers = UserAnswer.query.filter_by(user_id=current_user.id).all()
    quiz_results = []

    for user_answer in user_answers:
        quiz = Quiz.query.get(user_answer.quiz_id)
        correct_answers = 0

        # Kullanıcının her sorusu doğru mu kontrol ediliyor
        if user_answer.userOption == Question.query.get(user_answer.question_id).correct_option:
            correct_answers += 1

    quiz_results.append({
        'quiz_name': quiz.name,
        'score': correct_answers
    })

    return render_template('dashboard.html', quiz_results=quiz_results)


@app.route('/login_failed', methods=['GET'])
def login_failed():
    return render_template('login_failed.html')



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        # HTML formundan gelen şehir adını alın
        city = request.form['city']

        # API'den hava durumu verilerini çekin
        url = f'http://api.weatherapi.com/v1/forecast.json?key={"c46a7369afb341c88ba62039233008"}&q={city}&days=3&lang=tr'  # 3 günlük hava durumu verisi
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Hava durumu verilerini işleyin (örneğin, 3 günlük hava durumu)
            location = data['location']
            current = data['current']
            forecast = data['forecast']['forecastday']

            # Bugünkü hava durumu verileri
            current_weather = {
                'location_name': location['name'],
                'country': location['country'],
                'temperature_c': current['temp_c'],
                'temperature_f': current['temp_f'],
                'is_day': current['is_day'],
                'condition': current['condition']['text'],
                'wind_speed_kph': current['wind_kph'],
                'pressure_mb': current['pressure_mb'],
                'precipitation_mm': current['precip_mm'],
                'humidity': current['humidity'],
                'cloud': current['cloud'],
                'feelslike_c': current['feelslike_c'],
                'feelslike_f': current['feelslike_f'],
                'uv_index': current['uv'],
                'gust_kph': current['gust_kph']
            }

            # 3 günlük hava durumu verileri
            weather_forecast = []

            for day_data in forecast:
                date = day_data['date']
                max_temp_c = day_data['day']['maxtemp_c']
                min_temp_c = day_data['day']['mintemp_c']
                max_temp_f = day_data['day']['maxtemp_f']
                min_temp_f = day_data['day']['mintemp_f']
                condition = day_data['day']['condition']['text']
                uv_index = day_data['day']['uv']
                
                weather_forecast.append({
                    'date': date,
                    'max_temp_c': max_temp_c,
                    'min_temp_c': min_temp_c,
                    'max_temp_f': max_temp_f,
                    'min_temp_f': min_temp_f,
                    'condition': condition,
                    'uv_index': uv_index
                })

            return render_template('weather.html', current_weather=current_weather, weather_forecast=weather_forecast)

    return render_template('weather.html', current_weather=None, weather_forecast=None)


@app.route('/quizzes', methods=['GET', 'POST'])
def quizzes():
    datas=db.session.query(Quiz).all()
    return render_template('quizzes.html',quizzes=datas)


@app.route('/quiz/<int:quiz_number>/<int:question_number>', methods=['GET'])
@login_required
def quiz(quiz_number,question_number):
    try:
        data=db.session.query(Question).filter(Question.quiz_id==quiz_number,Question.id==question_number).one()
    except NoResultFound:
        return redirect(url_for('quizzes'))
    else:
        question_text=data.question_text
        options=[data.option1,data.option2,data.option3,data.option4]
        return render_template('quiz.html', quiz_number=quiz_number,question_number=question_number, question_text=question_text, options=options)


@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    # Kullanıcının seçtiği cevap
    selected_option = request.form.get('answer')
    quiz_number = int(request.form.get('quiz_number'))
    question_number = int(request.form.get('question_number'))
    # Kullanıcının cevabını saklayın (örneğin, veritabanına kaydedebilirsiniz)
    #user_answers[(quiz_number, question_number)] = selected_option

    # Bir sonraki soruya geçiş yapın (varsa)
    return redirect(url_for('quiz', quiz_number=quiz_number, question_number=question_number+1))

    '''if next_question_number <= len(quizzes[quiz_number]["questions"]):
        return redirect(url_for('quiz', quiz_number=quiz_number, question_number=next_question_number))
    else:
        pass
        # Tüm sorular yanıtlandıysa sonuçları gösterin
        #return render_template('quiz_result.html', quiz_number=quiz_number, user_answers=user_answers)'''



# Liderlik tablosu için işlev
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    # Tüm kullanıcıları al
    users = User.query.all()
    
    # Kullanıcıların skorlarını hesapla ve skora göre sırala
    leaderboard = []
    for user in users:
        user_score = calculate_user_score(user.id)
        leaderboard.append({'username': user.username, 'score': user_score})
    
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    return render_template('leaderboard.html', leaderboard=enumerate(leaderboard))

# Kullanıcının skorunu hesaplamak için işlev
def calculate_user_score(user_id):
    # Kullanıcının tüm cevaplarını al
    user_answers = UserAnswer.query.filter_by(user_id=user_id).all()
    
    # Kullanıcının doğru ve yanlış cevaplarını say
    correct_answers = 0
    wrong_answers = 0
    
    for answer in user_answers:
        question = Question.query.get(answer.question_id)
        if question.correct_option == answer.userOption:
            correct_answers += 1
        else:
            wrong_answers += 1
    
    # Skoru hesapla (örneğin, doğru cevapların sayısı)
    user_score = correct_answers
    
    return user_score