# IoT Sensor Health Monitor

**Lecture 1 — Python Programming Question: IoT Sensor Data**
Machine Learning and Deep Learning in IoT · MSc in Computer Science / IoT
University of Sumer — College of Computer Science and Information Technology · 2026–2027

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibrahimaldhaher/iot-sensor-health-monitor/blob/main/notebooks/01_sensor_monitoring.ipynb)
[![CI](https://github.com/ibrahimaldhaher/iot-sensor-health-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/ibrahimaldhaher/iot-sensor-health-monitor/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## The exercise

> Write a Python program that stores temperature and vibration measurements in two lists,
> calculates both averages, classifies each measurement as **Normal** or **Abnormal**
> (`Temperature > 80 °C` or `Vibration > 5.0` → Abnormal), prints the status of every
> measurement, and prints the total number of abnormal measurements.
>
> ```python
> temperature = [72, 75, 83, 78, 85]
> vibration   = [2.1, 3.0, 6.2, 2.8, 5.5]
> ```

### Answer

| | |
|---|---|
| Average temperature | **78.60 °C** |
| Average vibration | **3.92** |
| Abnormal measurements | **2 of 5** |
| Which ones | reading 3 (83 °C, 6.2) and reading 5 (85 °C, 5.5) — both break *both* limits |

---

## What is in this repository

The exercise is answered twice, on purpose.

**`solution.py`** is the literal answer: two lists, two averages, one rule, one counter.
No imports, no abstractions — the version that belongs on the answer sheet.

**`src/iot_monitor/`** is the same rule written the way it would be written for a device
that has to run it every second for a year:

- **Thresholds are data, not literals.** `Thresholds` is an immutable, validated object,
  so a different motor gets different limits without a code change — and the boundary
  behaviour becomes testable.
- **A verdict carries its reason.** `Abnormal` alone is not actionable; maintenance needs
  to know whether the motor is running *hot* or *shaking*. `Evaluation.breached` records
  which rule fired.
- **The comparison is strictly greater than.** A reading sitting exactly on the limit is
  still Normal — the wording of the exercise, and also the classic off-by-one of threshold
  monitoring: get it wrong and every machine running at its rated maximum raises a false
  alarm. Four parametrised tests pin that boundary down.
- **Formatting is separated from deciding**, so the same logic serves a notebook, a CLI
  and a JSON API without change.

**`notebooks/01_sensor_monitoring.ipynb`** runs both versions, visualises the result, and
then closes the loop with the lecture: it trains a decision tree on labelled data and shows
it recovering the same boundary a human wrote by hand (§1.4, *Rules + Data → Output* versus
*Data + Desired Output → Learned model*), reports precision/recall rather than accuracy
alone (§1.19), and ends on where the model should actually run (§1.16).

```
.
├── solution.py                    # the literal exam answer, zero dependencies
├── src/iot_monitor/
│   ├── config.py                  # Thresholds — validated, immutable
│   ├── models.py                  # Reading, Status, Evaluation, Summary
│   ├── analysis.py                # mean, evaluate_reading, evaluate_all, summarize
│   ├── data.py                    # lecture values + CSV loader
│   ├── report.py                  # text rendering
│   └── cli.py                     # python -m iot_monitor
├── notebooks/01_sensor_monitoring.ipynb
├── tests/                         # 27 tests: boundaries, empty input, CLI, CSV
├── data/lecture1_readings.csv
├── .devcontainer/ · .vscode/      # VS Code / Codespaces
└── .github/workflows/ci.yml       # ruff + pytest on Python 3.10 / 3.11 / 3.12
```

---

## Run it

### Google Colab — nothing to install

Click the **Open in Colab** badge above. The first cell clones this repository and puts it
on the path; every other cell runs unchanged.

### VS Code

```bash
git clone https://github.com/ibrahimaldhaher/iot-sensor-health-monitor.git
cd iot-sensor-health-monitor
code .
```

VS Code will offer the recommended extensions (Python, Ruff, Jupyter) and the
**Reopen in Container** action. In a container everything is installed for you; otherwise:

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev,notebook]"
```

Then `Run and Debug` offers two ready configurations — the exercise solution and the CLI —
and the Testing panel discovers the suite automatically.

### Command line

```bash
python solution.py                                    # the exam answer
python -m iot_monitor                                 # the engineered report
python -m iot_monitor --csv data/lecture1_readings.csv
python -m iot_monitor --temperature-limit 76 --vibration-limit 4.5
python -m iot_monitor --json                          # machine-readable
pytest                                                # 27 tests
```

The CLI exits `0` when the batch is clean, `1` when any reading is abnormal and `2` on a
bad input — so it drops straight into a cron job or a monitoring pipeline.

<details>
<summary>Sample output</summary>

```
PER-READING STATUS

#  Temperature (C)  Vibration  Status    Reason
-  ---------------  ---------  --------  ---------------------------------
1  72.0             2.10       Normal    within limits
2  75.0             3.00       Normal    within limits
3  83.0             6.20       Abnormal  temperature > 80 C, vibration > 5
4  78.0             2.80       Normal    within limits
5  85.0             5.50       Abnormal  temperature > 80 C, vibration > 5

SUMMARY

Readings analysed      : 5
Average temperature    : 78.60 C
Average vibration      : 3.92
Normal measurements    : 3
Abnormal measurements  : 2 (40% of the batch)
```

</details>

---

## Where the model should run (§1.16)

| | Cloud inference | Edge inference |
|---|---|---|
| Latency | network round-trip per reading | microseconds, local |
| Bandwidth | every raw sample transmitted | only alarms and summaries |
| Availability | no link, no decision | keeps deciding offline |
| Compute / memory | effectively unlimited | a few KB on an MCU |
| Model updates | one place to retrain and deploy | fleet-wide rollout problem |
| Privacy | raw data leaves the site | raw data stays on the machine |

A depth-3 decision tree is a handful of comparisons — it fits on the microcontroller bolted
to the motor. The honest architecture for this problem is therefore **edge inference, cloud
training**: the motor decides in place, and only labelled events travel upstream to improve
the next model.

---

<div dir="rtl">

## بالعربية

### الواجب

مطلوب برنامج بايثون يخزّن قياسات الحرارة والاهتزاز في قائمتين، ويحسب المعدّل لكل منهما،
ويحدّد لكل قياس إن كانت المكينة **طبيعية** أم **غير طبيعية**
(حرارة > 80 °م أو اهتزاز > 5.0 ⟵ غير طبيعية)، ثم يطبع الحالة لكل قياس ومجموع القياسات غير الطبيعية.

### الجواب

معدّل الحرارة **78.60 °م** · معدّل الاهتزاز **3.92** · عدد القياسات غير الطبيعية **2 من 5**
(القياس الثالث 83 °م و 6.2، والقياس الخامس 85 °م و 5.5 — وكلاهما يتجاوز الحدّين معاً).

### ليش نسختين من الحل؟

`solution.py` هو الجواب الحرفي للسؤال: قائمتان، معدّلان، شرط واحد، وعدّاد — بدون أي استيراد،
وهذا هو الشكل الذي يُسلَّم على الورقة.

أما `src/iot_monitor/` فهو نفس المنطق مكتوباً كما يُكتب لجهاز سيشغّله كل ثانية لمدة سنة:
الحدود صارت كائناً غير قابل للتعديل بدل أرقام مبعثرة داخل الشرط، والنتيجة تحمل **سببها**
(حرارة أم اهتزاز، لأن كلمة «غير طبيعية» وحدها لا تُبنى عليها صيانة)، والمقارنة **أكبر من**
بالمعنى الدقيق — فالقياس الواقع على الحدّ تماماً يبقى طبيعياً، وهذا الخطأ الشائع في أنظمة
الإنذار: لو انعكس لأصبحت كل مكينة تعمل على أقصى طاقتها المسموحة تطلق إنذاراً كاذباً.

### التشغيل

- **Colab:** اضغط شارة *Open in Colab* في الأعلى — الخلية الأولى تستنسخ المستودع وتضبط المسار، ولا شيء آخر يحتاج تثبيتاً.
- **VS Code:** استنسخ المستودع ثم `code .`؛ سيعرض عليك *Reopen in Container* والإضافات الموصى بها، وستجد إعدادَي تشغيل جاهزين في لوحة التصحيح.
- **الطرفية:** `python solution.py` للجواب المباشر، و`python -m iot_monitor` للنسخة الكاملة، و`pytest` لتشغيل 27 اختباراً.

### الجزء الأخير من النوتبوك

يدرّب شجرة قرار على بيانات موسومة ويُظهرها وهي تستعيد نفس الحدّ الذي كتبناه بأيدينا —
وهذا بالضبط الفرق الذي تشرحه الفقرة 1.4: البرمجة التقليدية تعطي القواعد لتحصل على النتيجة،
والتعلّم الآلي يعطي النتائج ليستخرج القاعدة. النتائج تُقرأ بـ precision و recall لا بالدقة
وحدها (فقرة 1.19)، وينتهي النوتبوك بالسؤال المعماري: أين يجب أن يعمل النموذج (فقرة 1.16).

</div>

---

## License

MIT — see [LICENSE](LICENSE).
