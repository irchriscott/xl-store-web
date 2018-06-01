package main

import (
	"database/sql"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

type CompanyCategories struct {
	ID          uint8  `json:"id"`
	Name        string `json:"name"`
	Image       string `json:"image"`
	Description string `json:"description"`
}

type Address struct {
	Address   string  `json:"address"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
}

type Categories struct {
	ID          int64  `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	CreatedDate string `json:"created_date"`
}

type Advertisments struct {
	ID          int64  `json:"id"`
	Description string `json:"description"`
	VideoURL    string `json:"video"`
	PostedDate  string `json:"posted_date"`
}

type Company struct {
	ID               int64             `json:"id"`
	Name             string            `json:"name"`
	NameURL          string            `json:"urlname"`
	Email            string            `json:"email"`
	ProfileImage     string            `json:"profile_image"`
	CoverImage       sql.NullString    `json:"cover_image"`
	PhoneNumber      string            `json:"phone_number"`
	Country          string            `json:"country"`
	Town             string            `json:"town"`
	CategoryID       uint8             `json:"category_id"`
	Category         CompanyCategories `json:"category"`
	Motto            sql.NullString    `json:"motto"`
	Description      sql.NullString    `json:"description"`
	IsAuthenticated  bool              `json:"is_authenticated"`
	HasSeenTuts      bool              `json:"has_seen_tutorial"`
	RegistrationDate string            `json:"registration_date"`
	Addresses        []Address         `json:"addresses"`
	URL              string            `json:"url"`
	Products         int64             `json:"products"`
	Followers        int64             `json:"followers"`
	Categories       int64             `json:"categories"`
	Posts            int64             `json:"posts"`
	Advertisments    int64             `json:"advertisments"`
}

func (company *Company) mGetCompanyProfile(db *sql.DB) error {

	q := "SELECT id, name, name_dotted, email, profile_image, cover_image, phone_number, country, town, motto, description, is_authenticated, registration_date, category_id, has_seen_tutorial  FROM xlstore_company WHERE id = ?"

	err := db.QueryRow(q, company.ID).Scan(
		&company.ID,
		&company.Name,
		&company.NameURL,
		&company.Email,
		&company.ProfileImage,
		&company.CoverImage,
		&company.PhoneNumber,
		&company.Country,
		&company.Town,
		&company.Motto,
		&company.Description,
		&company.IsAuthenticated,
		&company.RegistrationDate,
		&company.CategoryID,
		&company.HasSeenTuts,
	)

	company.Category = company.getCompanyCategory(db)
	company.Addresses = company.getCompanyAddresses(db)
	company.Products = company.getSumProducts(db)
	company.Posts = company.getSumPosts(db)
	company.Categories = company.getSumCategories(db)
	company.Followers = company.getSumFollowers(db)
	company.Advertisments = company.getSumAdvertisments(db)
	company.URL = company.getCompanyURL()

	if err != nil && err != sql.ErrNoRows {
		log.Fatal(err)
		panic(err.Error())
	}

	return err
}

func (company *Company) mGetCompanies(db *sql.DB) ([]Company, error) {

	q := "SELECT id, name, name_dotted, email, profile_image, cover_image, phone_number, country, town, motto, description, is_authenticated, registration_date, category_id, has_seen_tutorial  FROM xlstore_company"
	rows, err := db.Query(q)

	if err != nil {
		log.Fatal(err)
	}

	companies := []Company{}

	for rows.Next() {

		var company Company

		if err := rows.Scan(
			&company.ID,
			&company.Name,
			&company.NameURL,
			&company.Email,
			&company.ProfileImage,
			&company.CoverImage,
			&company.PhoneNumber,
			&company.Country,
			&company.Town,
			&company.Motto,
			&company.Description,
			&company.IsAuthenticated,
			&company.RegistrationDate,
			&company.CategoryID,
			&company.HasSeenTuts,
		); err != nil {

			return nil, err
		}

		company.Category = company.getCompanyCategory(db)
		company.Addresses = company.getCompanyAddresses(db)
		company.Products = company.getSumProducts(db)
		company.Posts = company.getSumPosts(db)
		company.Categories = company.getSumCategories(db)
		company.Followers = company.getSumFollowers(db)
		company.Advertisments = company.getSumAdvertisments(db)
		company.URL = company.getCompanyURL()

		companies = append(companies, company)
	}

	return companies, nil
}

func (category *Categories) mGetCategory(db *sql.DB) error {

	q := "SELECT id, name, description, created_date FROM xlstore_categories WHERE id = ?"
	err := db.QueryRow(q, category.ID).Scan(
		&category.ID,
		&category.Name,
		&category.Description,
		&category.CreatedDate,
	)

	if err != nil && err != sql.ErrNoRows {
		log.Fatal(err)
	}

	return err
}

//Company Attributes Functions

func (company *Company) getCompanyCategory(db *sql.DB) CompanyCategories {

	var compCategory CompanyCategories

	q := "SELECT * FROM xlstore_companycategories WHERE id = ?"

	category := db.QueryRow(q, company.CategoryID).Scan(
		&compCategory.ID,
		&compCategory.Name,
		&compCategory.Description,
		&compCategory.Image,
	)

	if category != nil && category != sql.ErrNoRows {
		panic(category.Error())
	}

	return compCategory
}

func (company *Company) getCompanyAddresses(db *sql.DB) []Address {

	var addresses []Address

	q := "SELECT address, latitude, longitude FROM xlstore_address WHERE company_id = ?"
	rows, err := db.Query(q, company.ID)

	if err != nil && err != sql.ErrNoRows {
		log.Fatal(err)
	}

	for rows.Next() {
		var address Address
		if err != rows.Scan(&address.Address, &address.Latitude, &address.Longitude) {
			log.Fatal(err)
		}
		addresses = append(addresses, address)
	}

	return addresses
}

func (company *Company) getSumProducts(db *sql.DB) (products int64) {

	q := "SELECT * FROM xlstore_products WHERE company_id = ? AND is_deleted = ? AND is_to_be_posted = ?"
	row, err := db.Query(q, company.ID, false, true)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		products++
	}

	return
}

func (company *Company) getSumPosts(db *sql.DB) (posts int64) {

	q := "SELECT * FROM xlstore_posts WHERE company_id = ? AND is_deleted = ?"
	row, err := db.Query(q, company.ID, false)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		posts++
	}

	return
}

func (company *Company) getSumCategories(db *sql.DB) (categories int64) {

	q := "SELECT * FROM xlstore_categories WHERE company_id = ?"
	row, err := db.Query(q, company.ID)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		categories++
	}

	return
}

func (company *Company) getSumFollowers(db *sql.DB) (followers int64) {

	q := "SELECT * FROM xlstore_followers WHERE company_id = ?"
	row, err := db.Query(q, company.ID)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		followers++
	}

	return
}

func (company *Company) getSumAdvertisments(db *sql.DB) (advertisments int64) {

	q := "SELECT xlstore_advertisments.*, xlstore_products.product_name FROM xlstore_advertisments "
	q += "INNER JOIN xlstore_products ON xlstore_advertisments.product_id = xlstore_products.id WHERE xlstore_products.company_id = ?"
	row, err := db.Query(q, company.ID)

	if err != nil {
		log.Fatal(err)
	}

	for row.Next() {
		advertisments++
	}

	return
}

func (company *Company) getCompanyURL() string {
	return "company/" + company.NameURL + "/"
}
