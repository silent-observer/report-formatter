# Автоматическое форматирование по ГОСТ-у
## Общее описание работы

Эта программа позволяет вам автоматически генерировать docx документы, оформленные в соответствии с
ГОСТ Р 7.0.100-2018. Для работы с ней вам потребуется написать файл в простом текстовом 
формате .md (Markdown, но с кастомными расширениями). Для генерации документа достаточно просто
перетащить .md файл на formatter.exe в папке. Далее будет описан сам формат Markdown

## Заголовки
Программа поддерживает 2 уровня заголовков: заголовки разделов и заголовки подразделов.
Чтобы указать заголовок раздела, достаточно написать
```markdown
# Заголовок раздела
```
Для заголовка подраздела соответственно
```markdown
## Заголовок подраздела
```
Нумерация проставляется автоматически, разделы и подразделы нумеровать не нужно. Также автоматически 
определяются структурные заголовки, например вы можете просто написать
```markdown
# Введение
```
и оно будет оформлено правильным образом.

## Основной текст
Просто пишите текст как обычно. По ГОСТу запрещено использовать **жирный шрифт**, но вы все еще 
можете его получить набрав `**текст**`. _Курсив_ можно получить набрав `_текст_`.

Каждый перенос строки в Markdown соответствует **переносу строки** в документе, обратите внимание,
не абзацу, а тому, что вы можете получить в MS Word комбинацией Shift+Enter. 
Чаще всего вы хотите не этого, а полноценный абзац. Для этого просто оставьте пустую 
строку между абзацами, вот так:
```markdown
Текст первого абзаца.

Текст второго абзаца.

Текст третьего абзаца.
```

## Уравнения
Форматтер имеет поддержку LaTeX. Это позволяет набирать уравнения прямо в текстовом файле, что особенно удобно, например, в VSCode с расширением Markdown+Math. Например если написать `$\frac{\pi}{\sqrt{2}}$`, успешно отобразится π/√2.

Вы также можете сделать себе пометку прямо внутри уравнения, чтобы исправить его на
полноценное уже в редакторе. Для этого необходимо после первого "$" поставить "!", например: 
`$!x = корень из 2$`. Это сгенерирует в документе уравнение с текстом 
"ВВЕДИТЕ УРАВНЕНИЕ(x = корень из 2)".

Вышеописанные уравнения - внутритекстовые уравнения. Если вам необходимо уравнение на отдельной
строчке, введите
```markdown
$$Текст уравнения$$
```

## Рисунки и таблицы
### Базовый вариант
Чтобы вставить рисунок, напишите
```markdown
!picture путь_к_файлу Название рисунка
```
например
```markdown
!picture image.png Красивая картинка
```
или
например
```markdown
!picture "длинный путь/с пробелами/image.png" Еще более красивая картинка
```
Таблицы с заполненными данными не поддерживаются (так как неудобны), но можно создать пустую
таблицу при помощи
```markdown
!table Название таблицы
```
### Размеры рисунков и таблиц
При необходимости вы можете указать ширину или высоту рисунка в сантиметрах, например
w10 - ширина 10 см, h1.3 - высота 1.3 см:
```markdown
!picture w10 image.png Красивая картинка
```
Стандартный размер таблицы: 3х4 (3 столбца, 4 строки), но его можно поменять, например,
это таблица 5х12:
```markdown
!table 5 12 Название второй таблицы
```
### Теги
Нумерация таблиц и рисунков происходит автоматически, но часто бывает необходимо сослаться на
какой-либо конкретный рисунок или таблицу. Чаще всего этот рисунок/таблица - просто следующий 
в этом подразделе. Тогда номер этого рисунка/таблицы можно получить соответственно как `!p!` или
`!t!`:
```markdown
...результаты вы можете увидеть в таблице !t!.
!table Результаты
```
Иногда все же нужно сослаться на какой-то другой рисунок/таблицу. Для этого существуют _теги_,
вы можете дать какому-то рисунку/таблице тег и потом ссылаться на него. Тег указывается в 
квадратных скобках сразу после picture/table, а номер таблицы можно получить как `!тег!`:
```markdown
!picture[very-important-picture] images/important.png Очень важный рисунок

...

Воспользуемся очень важными данными с рисунка !very-important-picture!.
```
### Тип нумерации
По умолчанию и для рисунков, и для таблиц используется сквозная (global) нумерация.
Возможно переключить тип нумерации на нумерацию по разделу (section) следующими командами:
Для рисунков:
```markdown
!picturenumbering = section
```
Для таблиц:
```markdown
!tablenumbering = section
```

## Код
Для вставки кусков кода используйте тройные символы `:
~~~
```
print('Hello world!')
```
~~~

## Содержание
Используется стандартное автоматическое содержание MS Word. Для вставки содержания напишите
```
!toc
```
в нужном месте. В итоговом документе появится область содержания с просьбой нажать на нее правой
кнопкой мыши и обновить поля. Это создаст содержание.

## Библиография
### Описание источника
В любом месте документа можно добавить описание источника через директиву book следующим образом:
```
.. book:: Название книги
    :поле1: Значение поля 1
    :поле2: Значение поля 2
    ...
```
Существуют несколько типов источников, для каждого из которых нужны свои поля.
Поля, используемые для всех источников:
* "Заголовок" (указывается сразу после `book::`, обязателен) - название источника.
* `:type:` - Тип источника (обязателен). Возможные значения: `book` (книга), `article` (статья), `website` (сайт),
  `webpage` (статья с сайта).
* `:author:` - Автор источника (не обязателен). Это поле может повторяться, авторы указываются в 
  порядке, указанном в самой книге, например: `Ф.М. Достоевский` или `К.И. Костенко`.
* `:city:` - Город издания (обязательно для книг), например, `Краснодар` или `М.`
* `:year:` - Год издания (обязательно для книг), например, `1970`.
* `:tag:` - Тэг (не обязательно), используется для ссылок на книгу.

Поля для типа `book` и `article`:
* `:other-people:` - Прочие люди (не обязательны), например, редакторы, переводчики и прочее. 
  Обычно указывается в самой книге, например, `под редакцией Иванова И.И.`
* `:title-info:` - Пояснение к названию (не обязательно), то, чем является источник, 
  например, `учебник`.
* `:edition:` - Сведения об издании (не обязательно), например, `2-е изд.`
* `:publisher:` - Издательство (обязательно для `book`), например, `Наука`.
* `:pages:` - Число страниц для `book` или страницы, где расположена статья для `article` (обязательно), например `573`.
* `:isbn:` - Номер ISBN (не обязательно), например `979-8566401997`.
* `:doi:` - Номер DOI (не обязательно), например `10.1029/2018JA025877`.

Поля для типа `article`:
* `:source:` - Исходный материал, откуда была взята статья, например `Proceedings of MILCOM '95`.
* `:volume:` - Номер тома, например `т.2`

Поля для типа `website` и `webpage`:
* `:url:` - Ссылка на страницу (обязательно), например, `https://ru.wikipedia.org`
* `:date:` или `:date-of-access:` - Дата обращения к странице (обязательно), например `10.03.2021`

Поля для типа `webpage`:
* `:website:` - Название сайта, откуда взята статья (обязательно), например 
  `Википедия, свободная энциклопедия`

### Ссылки
Если вы указали тэг у книги, то на нее можно сослаться, написав `[!тэг!]`, это превратится в
что-то типа `[42]`

### Список использованных источников
Напишите
```
!biblio
```
чтобы вставить список использованных источников. В нем будут указаны все описанные источники
в том порядке, в каком они встречаются в файле.