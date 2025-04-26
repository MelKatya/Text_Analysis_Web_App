from flask import Flask, request, render_template
from utils import sort_words_by_idf
from werkzeug.exceptions import RequestEntityTooLarge


ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    """
    Обрабатывает запрос к корневой странице сайта.

    Returns:
        HTML-шаблон "index.html" для отображения основной страницы.
    """
    return render_template("index.html")


@app.route('/text_analysis', methods=['GET', 'POST'])
def text_analysis():
    """
    Обрабатывает загрузку и анализ текстового файла.

    При POST-запросе:
        - Получает файл из формы
        - Выполняет анализ текста

    Returns:
        Шаблон с результатами анализа или страницу загрузки файла.
    """
    if request.method == 'POST':

        try:
            file = request.files["file"]
            if not file:
                raise FileNotFoundError

        except RequestEntityTooLarge as exc:
            mistake_text = ('Файл слишком большой. Пожалуйста, '
                            'выберите файл размером не более 256 КБ и попробуйте снова.')
            return render_template("redirect.html", mistake=mistake_text, exc=exc)

        if not allowed_file(file.filename):
            mistake_text = ('Допустим только текстовый файл формата .txt. '
                            'Пожалуйста, выберите правильный файл и попробуйте снова.')
            return render_template("redirect.html", mistake=mistake_text)

        file.save(file.filename)
        res_analysis = sort_words_by_idf(file.filename)

        return render_template("result_of_analysis.html", words=res_analysis)

    mistake_text = 'Чтобы проанализировать текст, загрузите файл на главной странице.'
    return render_template("redirect.html", mistake=mistake_text)


@app.errorhandler(FileNotFoundError)
def handle_exception(e: FileNotFoundError):
    mistake_text = ('Файл не был найден или загружен. '
                    'Пожалуйста, вернитесь на главную страницу и попробуйте снова.')

    return render_template("redirect.html", mistake=mistake_text)


if __name__ == '__main__':

    app.run(debug=True)
