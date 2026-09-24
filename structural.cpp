// Задача 10: Конвертер валют.
// Структурный стиль: данные (struct + vector) отдельно, логика — в функциях.

#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <limits>
#include <cctype>

using namespace std;

// Базовая валюта: курсы всех остальных задаются по отношению к ней.
const string BASE_CODE = "BYN";

// Данные о валюте: код и сколько базовой валюты стоит 1 её единица.
struct CurrencyRate {
    string code;
    double rateToBase;
};

// Приводим код к верхнему регистру и убираем пробелы по краям.
string normalizeCode(const string& raw) {
    string result;
    for (char ch : raw) {
        if (!isspace(static_cast<unsigned char>(ch))) {
            result += static_cast<char>(toupper(static_cast<unsigned char>(ch)));
        }
    }
    return result;
}

// Позиция валюты в списке или -1, если её нет.
int findIndex(const vector<CurrencyRate>& rates, const string& code) {
    for (size_t i = 0; i < rates.size(); ++i) {
        if (rates[i].code == code) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

// Задать новый курс или обновить существующий.
bool setRate(vector<CurrencyRate>& rates, const string& rawCode, double rate, string& error) {
    string code = normalizeCode(rawCode);

    if (code.empty()) {
        error = "Код валюты не может быть пустым";
        return false;
    }
    if (rate <= 0.0) {
        error = "Курс должен быть положительным";
        return false;
    }
    // Курс базовой валюты к самой себе всегда равен единице.
    if (code == BASE_CODE && rate != 1.0) {
        error = "Курс базовой валюты " + BASE_CODE + " всегда равен 1";
        return false;
    }

    int index = findIndex(rates, code);
    if (index >= 0) {
        rates[index].rateToBase = rate;
    } else {
        CurrencyRate item;
        item.code = code;
        item.rateToBase = rate;
        rates.push_back(item);
    }
    return true;
}

// Получить курс валюты к базовой.
bool getRate(const vector<CurrencyRate>& rates, const string& rawCode, double& rate, string& error) {
    string code = normalizeCode(rawCode);
    int index = findIndex(rates, code);
    if (index < 0) {
        error = "Валюта " + code + " не найдена";
        return false;
    }
    rate = rates[index].rateToBase;
    return true;
}

// Конвертация A -> B через базовую валюту.
bool convert(const vector<CurrencyRate>& rates, double amount,
             const string& fromCode, const string& toCode,
             double& result, string& error) {
    if (amount < 0.0) {
        error = "Сумма не может быть отрицательной";
        return false;
    }

    double fromRate = 0.0;
    double toRate = 0.0;
    if (!getRate(rates, fromCode, fromRate, error)) return false;
    if (!getRate(rates, toCode, toRate, error)) return false;

    double amountInBase = amount * fromRate;  // сначала переводим в базовую
    result = amountInBase / toRate;           // затем из базовой в целевую
    return true;
}

// Список доступных валют с курсами.
void printCurrencies(const vector<CurrencyRate>& rates) {
    cout << "\nДоступные валюты (курс к " << BASE_CODE << "):\n";
    if (rates.empty()) {
        cout << "  список пуст\n";
        return;
    }
    for (const CurrencyRate& item : rates) {
        cout << "  " << item.code << " -> "
             << fixed << setprecision(4) << item.rateToBase << " " << BASE_CODE << "\n";
    }
}

// Заполняем справочник стартовыми курсами.
void loadDefaultRates(vector<CurrencyRate>& rates) {
    string error;
    setRate(rates, BASE_CODE, 1.0, error);
    setRate(rates, "USD", 3.2500, error);
    setRate(rates, "EUR", 3.5100, error);
    setRate(rates, "PLN", 0.8200, error);
    setRate(rates, "RUB", 0.0350, error);
}

// Демонстрационный сценарий: показывает все операции без участия пользователя.
void runDemo(vector<CurrencyRate>& rates) {
    string error;
    double result = 0.0;

    cout << "===== ДЕМОНСТРАЦИЯ (структурный стиль) =====\n";
    printCurrencies(rates);

    cout << "\n1) Конвертация 100 USD в BYN:\n";
    if (convert(rates, 100.0, "USD", "BYN", result, error)) {
        cout << "   100 USD = " << fixed << setprecision(2) << result << " BYN\n";
    }

    cout << "2) Конвертация 500 PLN в EUR (через базу):\n";
    if (convert(rates, 500.0, "PLN", "EUR", result, error)) {
        cout << "   500 PLN = " << fixed << setprecision(2) << result << " EUR\n";
    }

    cout << "3) Обновляем курс USD с 3.25 на 3.40:\n";
    if (setRate(rates, "usd", 3.40, error)) {
        cout << "   курс обновлён\n";
    }
    if (convert(rates, 100.0, "USD", "BYN", result, error)) {
        cout << "   теперь 100 USD = " << fixed << setprecision(2) << result << " BYN\n";
    }

    cout << "4) Добавляем новую валюту GBP по курсу 4.15:\n";
    if (setRate(rates, "GBP", 4.15, error)) {
        cout << "   валюта добавлена\n";
    }

    cout << "5) Проверка ошибок:\n";
    if (!setRate(rates, "CHF", -1.0, error)) {
        cout << "   отрицательный курс: " << error << "\n";
    }
    if (!convert(rates, 10.0, "USD", "JPY", result, error)) {
        cout << "   неизвестная валюта: " << error << "\n";
    }

    printCurrencies(rates);
    cout << "===== КОНЕЦ ДЕМОНСТРАЦИИ =====\n\n";
}

// Читаем строку, отбрасывая остаток предыдущей строки ввода.
string readLine(const string& prompt) {
    cout << prompt;
    string line;
    getline(cin, line);
    return line;
}

// Читаем число с проверкой ввода.
bool readNumber(const string& prompt, double& value) {
    string line = readLine(prompt);
    try {
        size_t pos = 0;
        value = stod(line, &pos);
        return pos == line.size() || isspace(static_cast<unsigned char>(line[pos]));
    } catch (...) {
        cout << "Нужно ввести число\n";
        return false;
    }
}

void runMenu(vector<CurrencyRate>& rates) {
    while (true) {
        cout << "\n--- Конвертер валют ---\n"
             << "1. Задать/обновить курс\n"
             << "2. Конвертировать сумму\n"
             << "3. Список валют\n"
             << "0. Выход\n";

        string choice = readLine("Выбор: ");
        string error;

        if (choice == "1") {
            string code = readLine("Код валюты: ");
            double rate = 0.0;
            if (!readNumber("Курс к " + BASE_CODE + ": ", rate)) continue;
            if (setRate(rates, code, rate, error)) {
                cout << "Курс сохранён\n";
            } else {
                cout << "Ошибка: " << error << "\n";
            }
        } else if (choice == "2") {
            double amount = 0.0;
            if (!readNumber("Сумма: ", amount)) continue;
            string from = readLine("Из валюты: ");
            string to = readLine("В валюту: ");
            double result = 0.0;
            if (convert(rates, amount, from, to, result, error)) {
                cout << fixed << setprecision(2) << amount << " " << normalizeCode(from)
                     << " = " << result << " " << normalizeCode(to) << "\n";
            } else {
                cout << "Ошибка: " << error << "\n";
            }
        } else if (choice == "3") {
            printCurrencies(rates);
        } else if (choice == "0") {
            cout << "Выход\n";
            return;
        } else {
            cout << "Нет такого пункта\n";
        }
    }
}

int main() {
    vector<CurrencyRate> rates;
    loadDefaultRates(rates);

    runDemo(rates);
    runMenu(rates);
    return 0;
}
