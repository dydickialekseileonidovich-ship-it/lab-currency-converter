// Задача 10: Конвертер валют.
// ООП-стиль: состояние спрятано в объектах, каждый класс отвечает за свою часть.

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <stdexcept>
#include <iomanip>
#include <cctype>

using namespace std;

// Небольшой помощник: нормализация кода валюты.
class CurrencyCode {
public:
    static string normalize(const string& raw) {
        string result;
        for (char ch : raw) {
            if (!isspace(static_cast<unsigned char>(ch))) {
                result += static_cast<char>(toupper(static_cast<unsigned char>(ch)));
            }
        }
        if (result.empty()) {
            throw invalid_argument("Код валюты не может быть пустым");
        }
        return result;
    }
};

// Валюта знает свой код и свой курс, сама следит за их корректностью.
class Currency {
public:
    Currency(const string& code, double rateToBase)
        : code_(CurrencyCode::normalize(code)) {
        setRateToBase(rateToBase);
    }

    const string& code() const { return code_; }
    double rateToBase() const { return rateToBase_; }

    void setRateToBase(double rate) {
        if (rate <= 0.0) {
            throw invalid_argument("Курс должен быть положительным");
        }
        rateToBase_ = rate;
    }

    // Перевод суммы этой валюты в базовую и обратно — знание самой валюты.
    double toBase(double amount) const { return amount * rateToBase_; }
    double fromBase(double amountInBase) const { return amountInBase / rateToBase_; }

private:
    string code_;
    double rateToBase_;
};

// Справочник валют: хранит курсы и умеет конвертировать через базовую валюту.
class CurrencyConverter {
public:
    explicit CurrencyConverter(const string& baseCode = "BYN")
        : baseCode_(CurrencyCode::normalize(baseCode)) {
        rates_.emplace(baseCode_, Currency(baseCode_, 1.0));
    }

    const string& baseCode() const { return baseCode_; }

    // Задать новый курс или обновить существующий.
    void setRate(const string& rawCode, double rate) {
        string code = CurrencyCode::normalize(rawCode);
        if (code == baseCode_ && rate != 1.0) {
            throw invalid_argument("Курс базовой валюты " + baseCode_ + " всегда равен 1");
        }

        auto it = rates_.find(code);
        if (it != rates_.end()) {
            it->second.setRateToBase(rate);
        } else {
            rates_.emplace(code, Currency(code, rate));
        }
    }

    bool has(const string& rawCode) const {
        return rates_.count(CurrencyCode::normalize(rawCode)) > 0;
    }

    const Currency& currency(const string& rawCode) const {
        string code = CurrencyCode::normalize(rawCode);
        auto it = rates_.find(code);
        if (it == rates_.end()) {
            throw invalid_argument("Валюта " + code + " не найдена");
        }
        return it->second;
    }

    // Конвертация A -> B: сначала в базовую валюту, затем в целевую.
    double convert(double amount, const string& fromCode, const string& toCode) const {
        if (amount < 0.0) {
            throw invalid_argument("Сумма не может быть отрицательной");
        }
        const Currency& from = currency(fromCode);
        const Currency& to = currency(toCode);
        return to.fromBase(from.toBase(amount));
    }

    // Список валют в алфавитном порядке (map хранит ключи отсортированными).
    vector<Currency> currencies() const {
        vector<Currency> list;
        for (const auto& pair : rates_) {
            list.push_back(pair.second);
        }
        return list;
    }

private:
    string baseCode_;
    map<string, Currency> rates_;
};

// Класс отвечает только за диалог с пользователем, расчётов в нём нет.
class ConverterApp {
public:
    explicit ConverterApp(CurrencyConverter& converter) : converter_(converter) {}

    void showCurrencies() const {
        cout << "\nДоступные валюты (курс к " << converter_.baseCode() << "):\n";
        for (const Currency& item : converter_.currencies()) {
            cout << "  " << item.code() << " -> "
                 << fixed << setprecision(4) << item.rateToBase()
                 << " " << converter_.baseCode() << "\n";
        }
    }

    void runDemo() {
        cout << "===== ДЕМОНСТРАЦИЯ (ООП-стиль) =====\n";
        showCurrencies();

        cout << "\n1) Конвертация 100 USD в BYN:\n";
        cout << "   100 USD = " << fixed << setprecision(2)
             << converter_.convert(100.0, "USD", "BYN") << " BYN\n";

        cout << "2) Конвертация 500 PLN в EUR (через базу):\n";
        cout << "   500 PLN = " << fixed << setprecision(2)
             << converter_.convert(500.0, "PLN", "EUR") << " EUR\n";

        cout << "3) Обновляем курс USD с 3.25 на 3.40:\n";
        converter_.setRate("usd", 3.40);
        cout << "   теперь 100 USD = " << fixed << setprecision(2)
             << converter_.convert(100.0, "USD", "BYN") << " BYN\n";

        cout << "4) Добавляем новую валюту GBP по курсу 4.15:\n";
        converter_.setRate("GBP", 4.15);
        cout << "   валюта добавлена\n";

        cout << "5) Проверка ошибок:\n";
        try {
            converter_.setRate("CHF", -1.0);
        } catch (const invalid_argument& e) {
            cout << "   отрицательный курс: " << e.what() << "\n";
        }
        try {
            converter_.convert(10.0, "USD", "JPY");
        } catch (const invalid_argument& e) {
            cout << "   неизвестная валюта: " << e.what() << "\n";
        }

        showCurrencies();
        cout << "===== КОНЕЦ ДЕМОНСТРАЦИИ =====\n\n";
    }

    void runMenu() {
        while (true) {
            cout << "\n--- Конвертер валют ---\n"
                 << "1. Задать/обновить курс\n"
                 << "2. Конвертировать сумму\n"
                 << "3. Список валют\n"
                 << "0. Выход\n";

            string choice = readLine("Выбор: ");

            try {
                if (choice == "1") {
                    string code = readLine("Код валюты: ");
                    double rate = readNumber("Курс к " + converter_.baseCode() + ": ");
                    converter_.setRate(code, rate);
                    cout << "Курс сохранён\n";
                } else if (choice == "2") {
                    double amount = readNumber("Сумма: ");
                    string from = readLine("Из валюты: ");
                    string to = readLine("В валюту: ");
                    double result = converter_.convert(amount, from, to);
                    cout << fixed << setprecision(2) << amount << " "
                         << CurrencyCode::normalize(from) << " = " << result << " "
                         << CurrencyCode::normalize(to) << "\n";
                } else if (choice == "3") {
                    showCurrencies();
                } else if (choice == "0") {
                    cout << "Выход\n";
                    return;
                } else {
                    cout << "Нет такого пункта\n";
                }
            } catch (const invalid_argument& e) {
                cout << "Ошибка: " << e.what() << "\n";
            }
        }
    }

private:
    CurrencyConverter& converter_;

    static string readLine(const string& prompt) {
        cout << prompt;
        string line;
        getline(cin, line);
        return line;
    }

    static double readNumber(const string& prompt) {
        string line = readLine(prompt);
        try {
            return stod(line);
        } catch (...) {
            throw invalid_argument("Нужно ввести число");
        }
    }
};

int main() {
    CurrencyConverter converter("BYN");
    converter.setRate("USD", 3.2500);
    converter.setRate("EUR", 3.5100);
    converter.setRate("PLN", 0.8200);
    converter.setRate("RUB", 0.0350);

    ConverterApp app(converter);
    app.runDemo();
    app.runMenu();
    return 0;
}
