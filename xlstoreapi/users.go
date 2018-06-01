package main

import (
	"database/sql"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

type User struct {
	Token            int64          `json:"token"`
	Name             string         `json:"name"`
	Username         string         `json:"username"`
	Email            string         `json:"email"`
	ProfileImage     string         `json:"profile_image"`
	CoverImage       sql.NullString `json:"cover_image"`
	Gender           string         `json:"gender"`
	Country          string         `json:"country"`
	Town             string         `json:"town"`
	PhoneNumber      sql.NullString `json:"phone_number"`
	Address          Address        `json:"address"`
	RegistrationDate string         `json:"registration_date"`
	URL              string         `json:"url"`
	Posts            int64          `json:"posts"`
	Following        int64          `json:"following"`
	Followers        int64          `json:"followers"`
	Companies        int64          `json:"companies"`
	Interess         int64          `json:"interess"`
	Replies          int64          `json:"replies"`
	Comments         int64          `json:"comments"`
	Likes            int64          `json:"likes"`
	Dislikes         int64          `json:"dislikes"`
	Trades           int64          `json:"trades"`
	Categories       int64          `json:"categories"`
	BillsCarts       int64          `json:"bills_carts"`
}

type UserAuthentication struct {
	Email    string `json:"Email"`
	Password string `json:"Password"`
}

func (user *User) mGetUserProfile(db *sql.DB) error {

	q := "SELECT id, full_name, user_name, email, profile_image, cover_image, gender, country, town, registration_date FROM xlstore_user WHERE id = ? OR email = ?"
	err := db.QueryRow(q, user.Token, user.Email).Scan(
		&user.Token,
		&user.Name,
		&user.Username,
		&user.Email,
		&user.ProfileImage,
		&user.CoverImage,
		&user.Gender,
		&user.Country,
		&user.Town,
		&user.RegistrationDate,
	)

	user.Address = user.getUserAddress(db)
	user.URL = user.getUserURL()
	user.Posts = user.getSumPosts(db)
	user.Following = user.getSumFollowing(db)
	user.Followers = user.getSumFollowers(db)
	user.Companies = user.getSumCompanies(db)
	user.Interess = user.getSumInteress(db)
	user.Replies = user.getSumReplies(db)
	user.Comments = user.getSumComments(db)
	user.Likes = user.getSumLikes(db)
	user.Dislikes = user.getSumDislikes(db)

	if err != nil && err != sql.ErrNoRows {
		log.Fatal(err)
	}

	return err
}

func (user *User) mGetUsers(db *sql.DB) ([]User, error) {

	users := []User{}

	q := "SELECT id, full_name, user_name, email, profile_image, cover_image, gender, country, town, registration_date FROM xlstore_user"
	rows, err := db.Query(q)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {

		var user User

		if err := rows.Scan(
			&user.Token,
			&user.Name,
			&user.Username,
			&user.Email,
			&user.ProfileImage,
			&user.CoverImage,
			&user.Gender,
			&user.Country,
			&user.Town,
			&user.RegistrationDate,
		); err != nil {
			return nil, err
		}

		user.Address = user.getUserAddress(db)
		user.URL = user.getUserURL()
		user.Posts = user.getSumPosts(db)
		user.Following = user.getSumFollowing(db)
		user.Followers = user.getSumFollowers(db)
		user.Companies = user.getSumCompanies(db)
		user.Interess = user.getSumInteress(db)
		user.Replies = user.getSumReplies(db)
		user.Comments = user.getSumComments(db)
		user.Likes = user.getSumLikes(db)
		user.Dislikes = user.getSumDislikes(db)

		users = append(users, user)
	}

	return users, nil
}

func (user *User) mRegisterUser(db *sql.DB) (token int64, err error) {

	q := "INSERT INTO xlstore_user(full_name, user_name, email, country, town, gender, password) "
	q += "VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id"

	err = db.QueryRow(q, &user.Name, &user.Username, &user.Email, &user.Country, &user.Town, &user.Gender).Scan(user.Token)

	if err != nil {
		log.Fatal(err)
	}

	token = user.Token
	return
}

func (userAuth *UserAuthentication) mUserAuthentication(db *sql.DB) error {

	var user User
	var password string

	q := "SELECT id, full_name, user_name, email, profile_image, cover_image, gender, country, town, registration_date, password FROM xlstore_user WHERE email = ?"
	err := db.QueryRow(q, userAuth.Email).Scan(
		&user.Token,
		&user.Name,
		&user.Username,
		&user.Email,
		&user.ProfileImage,
		&user.CoverImage,
		&user.Gender,
		&user.Country,
		&user.Town,
		&user.RegistrationDate,
		&password,
	)

	user.Address = user.getUserAddress(db)
	user.URL = user.getUserURL()
	user.Posts = user.getSumPosts(db)
	user.Following = user.getSumFollowing(db)
	user.Followers = user.getSumFollowers(db)
	user.Companies = user.getSumCompanies(db)
	user.Interess = user.getSumInteress(db)
	user.Replies = user.getSumReplies(db)
	user.Comments = user.getSumComments(db)
	user.Likes = user.getSumLikes(db)
	user.Dislikes = user.getSumDislikes(db)

	if err != nil && err != sql.ErrNoRows {
		log.Fatal(err)
	}

	if password == userAuth.Password {
		return err
	}

	return sql.ErrNoRows
}

func (user *User) checkUser(db *sql.DB) error {

	var userID int64
	q := "SELECT id FROM xlstore_user WHERE id = ?"
	err := db.QueryRow(q, &user.Token).Scan(&userID)

	return err
}

//User Attributes Functions

func (user *User) getUserAddress(db *sql.DB) Address {

	var address Address

	q := "SELECT address, latitude, longitude FROM xlstore_address WHERE user_id = ? LIMIT 1"
	err := db.QueryRow(q, user.Token).Scan(&address.Address, &address.Latitude, &address.Longitude)

	if err != nil && err != sql.ErrNoRows {
		log.Fatal(err)
	}

	return address
}

func (user *User) getSumPosts(db *sql.DB) (posts int64) {

	q := "SELECT * FROM xlstore_posts WHERE user_id = ? AND is_deleted = ?"
	rows, err := db.Query(q, user.Token, false)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		posts++
	}
	return
}

func (user *User) getSumFollowing(db *sql.DB) (folliwong int64) {

	q := "SELECT * FROM xlstore_userfollow WHERE follower_user_id = ?"
	rows, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		folliwong++
	}

	return
}

func (user *User) getSumFollowers(db *sql.DB) (followers int64) {

	q := "SELECT * FROM xlstore_userfollow WHERE following_id = ?"
	rows, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		followers++
	}

	return
}

func (user *User) getSumCompanies(db *sql.DB) (companies int64) {

	q := "SELECT * FROM xlstore_followers WHERE user_id = ?"
	row, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		companies++
	}

	return
}

func (user *User) getSumInteress(db *sql.DB) (interess int64) {

	q := "SELECT * FROM xlstore_productinteress WHERE user_id = ?"
	row, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		interess++
	}

	return
}

func (user *User) getSumReplies(db *sql.DB) (replies int64) {

	q := "SELECT * FROM xlstore_postreplies WHERE user_id = ?"
	row, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		replies++
	}

	return
}

func (user *User) getSumComments(db *sql.DB) (comments int64) {

	q := "SELECT * FROM xlstore_productcomments WHERE user_id = ?"
	row, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		comments++
	}

	return
}

func (user *User) getSumLikes(db *sql.DB) (likes int64) {

	q := "SELECT * FROM xlstore_productmention WHERE user_id = ? AND mention = 'like'"
	row, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		likes++
	}

	return
}

func (user *User) getSumDislikes(db *sql.DB) (dislikes int64) {

	q := "SELECT * FROM xlstore_productmention WHERE user_id = ? AND mention = 'dislike'"
	row, err := db.Query(q, user.Token)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		dislikes++
	}

	return
}

func (user *User) getUserURL() string {
	return "user/" + user.Username + "/"
}
