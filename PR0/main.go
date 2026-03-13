package main

import "fmt"

// Notifier определяет интерфейс для отправки уведомлений.
type Notifier interface {
	Send(message string) error
}

// EmailNotifier отправляет уведомления по email.
type EmailNotifier struct {
	smtpHost string
	smtpPort int
}

// Send реализует интерфейс Notifier для EmailNotifier.
func (e EmailNotifier) Send(message string) error {
	fmt.Printf("Sending email via %s:%d: %s\n", e.smtpHost, e.smtpPort, message)
	// Здесь была бы реальная отправка email
	return nil
}

// SmsNotifier отправляет уведомления через SMS.
type SmsNotifier struct {
	apiKey      string
	phoneNumber string
}

// Send реализует интерфейс Notifier для SmsNotifier.
func (s SmsNotifier) Send(message string) error {
	fmt.Printf("Sending SMS to %s using API key %s: %s\n", s.phoneNumber, s.apiKey, message)
	// Здесь была бы реальная отправка SMS
	return nil
}

// UserTereschukMax представляет пользователя, который может получать уведомления.
type UserTereschukMax struct {
	name     string
	email    string
	notifier Notifier // Зависимость от интерфейса (инъекция зависимости)
}

// NewUser создает нового пользователя с заданным способом уведомления.
func NewUser(name string, email string, notifier Notifier) *UserTereschukMax {
	return &UserTereschukMax{
		name:     name,
		email:    email,
		notifier: notifier,
	}
}

// Notify отправляет пользователю уведомление через его notifier.
func (u UserTereschukMax) Notify(message string) error {
	fmt.Printf("User %s (%s) received a notification: ", u.name, u.email)
	return u.notifier.Send(message)
}

func main() {
	// Создаем два способа уведомления
	emailNoti := EmailNotifier{smtpHost: "smtp.gmail.com", smtpPort: 587}
	smsNoti := SmsNotifier{apiKey: "12345", phoneNumber: "+79991112233"}

	// Создаем пользователей с разными способами уведомления
	user1 := NewUser("Alice", "alice@example.com", emailNoti)
	user2 := NewUser("Bob", "bob@example.com", smsNoti)

	// Отправляем уведомления
	user1.Notify("Hello, Alice!")
	user2.Notify("Hello, Bob!")
}