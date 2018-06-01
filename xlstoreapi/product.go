package main

import (
	"database/sql"
	"errors"
	"fmt"
	"log"
	"strconv"
	"time"
)

type OtherImages struct {
	ImageURL string `json:"image"`
}

type Product struct {
	ID            int64           `json:"id"`
	CompanyID     int64           `json:"company_id"`
	Company       Company         `json:"company"`
	Name          string          `json:"name"`
	CategoryID    int64           `json:"category_id"`
	Category      Categories      `json:"category"`
	Image         string          `json:"image"`
	Price         float64         `json:"price"`
	Currency      string          `json:"currency"`
	Description   string          `json:"description"`
	PostedDate    string          `json:"posted_date"`
	Advertisment  []Advertisments `json:"advertisment"`
	OtherImages   []OtherImages   `json:"other_images"`
	Interess      int64           `json:"interess"`
	Comments      int64           `json:"comments"`
	Likes         int64           `json:"likes"`
	Dislikes      int64           `json:"dislikes"`
	Mentions      []Mention       `json:"mentions"`
	UserInterests []Interess      `json:"user_interests"`
}

type Interess struct {
	ProductID    int64  `json:"product_id"`
	UserID       int64  `json:"user_id"`
	InteressDate string `json:"interess_date"`
}

type Mention struct {
	ProductID   int64  `json:"product_id"`
	UserID      int64  `json:"user_id"`
	Mention     string `json:"mention"`
	MentionDate string `json:"mention_date"`
}

type Comment struct {
	ID          int64         `json:"id"`
	ProductID   int64         `json:"product_id"`
	CompanyID   sql.NullInt64 `json:"company_id"`
	UserID      sql.NullInt64 `json:"user_id"`
	Company     Company       `json:"company"`
	User        User          `json:"user"`
	Commenter   string        `json:"commenter"`
	Comment     string        `json:"comment"`
	CommentDate string        `json:"comment_date"`
}

func (product *Product) mGetSingleProduct(db *sql.DB) error {

	q := "SELECT id, company_id, product_name, category, image, price, currency, product_description, posted_date FROM xlstore_products "
	q += "WHERE id = ? AND is_to_be_posted = ? AND is_deleted = ?"

	err := db.QueryRow(q, product.ID, true, false).Scan(
		&product.ID,
		&product.CompanyID,
		&product.Name,
		&product.CategoryID,
		&product.Image,
		&product.Price,
		&product.Currency,
		&product.Description,
		&product.PostedDate,
	)

	if err != nil {
		return err
	}

	company := Company{ID: product.CompanyID}
	category := Categories{ID: product.CategoryID}
	mention := Mention{ProductID: product.ID}
	interest := Interess{ProductID: product.ID}

	if err := company.mGetCompanyProfile(db); err != nil {
		log.Fatal(err)
	}

	if err := category.mGetCategory(db); err != nil {
		log.Fatal(err)
	}

	product.Company = company
	product.Category = category
	product.Advertisment = product.getProductAdvertisment(db)
	product.OtherImages = product.getProductPictures(db)
	product.Interess = product.getProductSumInteress(db)
	product.Comments = product.getProductSumComments(db)
	product.Likes = product.getProductSumLikes(db)
	product.Dislikes = product.getProductSumDislikes(db)
	product.Mentions = mention.getProductMentions(db)
	product.UserInterests = interest.getProductInterests(db)

	return err
}

func (product *Product) mGetProducts(db *sql.DB) ([]Product, error) {

	q := "SELECT id, company_id, product_name, category, image, price, currency, product_description, posted_date FROM xlstore_products "
	q += "WHERE is_to_be_posted = ? AND is_deleted = ? ORDER BY posted_date DESC"

	rows, err := db.Query(q, true, false)

	if err != nil {
		log.Fatal(err)
	}

	products := []Product{}

	for rows.Next() {
		var product Product

		if err := rows.Scan(
			&product.ID,
			&product.CompanyID,
			&product.Name,
			&product.CategoryID,
			&product.Image,
			&product.Price,
			&product.Currency,
			&product.Description,
			&product.PostedDate,
		); err != nil {
			return nil, err
		}

		company := Company{ID: product.CompanyID}
		category := Categories{ID: product.CategoryID}
		mention := Mention{ProductID: product.ID}
		interest := Interess{ProductID: product.ID}

		if err := company.mGetCompanyProfile(db); err != nil {
			return nil, err
		}

		if err := category.mGetCategory(db); err != nil {
			log.Fatal(err)
		}

		product.Company = company
		product.Category = category
		product.Advertisment = product.getProductAdvertisment(db)
		product.OtherImages = product.getProductPictures(db)
		product.Interess = product.getProductSumInteress(db)
		product.Comments = product.getProductSumComments(db)
		product.Likes = product.getProductSumLikes(db)
		product.Dislikes = product.getProductSumDislikes(db)
		product.Mentions = mention.getProductMentions(db)
		product.UserInterests = interest.getProductInterests(db)

		products = append(products, product)
	}
	return products, nil
}

func (product *Product) checkProduct(db *sql.DB) (int64, error) {

	var productID int64
	var companyID int64

	q := "SELECT id, company_id FROM xlstore_products WHERE id = ?"
	err := db.QueryRow(q, &product.ID).Scan(&productID, &companyID)

	return companyID, err
}

func (interess *Interess) mInteressProduct(db *sql.DB) (string, error) {

	var response string
	var about = "interess"
	today := time.Now().UTC()

	q := "SELECT id FROM xlstore_productinteress WHERE user_id = ? AND product_id = ?"
	err := db.QueryRow(q, interess.UserID, interess.ProductID).Scan(&response)

	if err != nil {

		product := Product{ID: interess.ProductID}
		user := User{Token: interess.UserID}

		if userID := user.checkUser(db); userID != nil {
			switch userID {
			case sql.ErrNoRows:
				return "User Not Found", sql.ErrNoRows
			default:
				return "Something Went Wrong", err
			}
		}

		companyID, err := product.checkProduct(db)

		if err != nil {
			switch err {
			case sql.ErrNoRows:
				return "Product Not Found", sql.ErrNoRows
			default:
				return "Something Went Wrong", err
			}
		}

		insq := "INSERT INTO xlstore_productinteress (user_id, product_id, interess_date) "
		insq += "VALUES (?,?,?)"

		stmt, err := db.Prepare(insq)

		defer stmt.Close()

		if err != nil {
			return "Error While Preparing Statement", err
		}

		res, err := stmt.Exec(&interess.UserID, &interess.ProductID, &today)

		if err != nil {
			return "Error While Excecuting Statement", err
		}

		notq := "INSERT INTO xlstore_companynotifications (notification_id, concern_id, user_id, about, posted_date) "
		notq += "VALUES (?,?,?,?,?)"

		inserr := db.QueryRow(notq, &interess.ProductID, &companyID, &interess.UserID, &about, &interess.InteressDate)

		if inserr != nil {
			return "Error While Inserting Notification", errors.New("Insrtion Error")
		}

		interessID, err := res.LastInsertId()

		if err != nil {
			return "Error While Getting Last Inserted ID", err
		}

		return strconv.FormatInt(interessID, 10), nil

	}

	return response, nil
}

func (mention *Mention) mMentionProduct(db *sql.DB) (string, error) {

	var response string
	today := time.Now().UTC()
	q := "SELECT id FROM xlstore_productmention WHERE product_id = ? AND user_id = ?"
	err := db.QueryRow(q, &mention.ProductID, &mention.UserID).Scan(&response)

	if err != nil {

		product := Product{ID: mention.ProductID}
		user := User{Token: mention.UserID}

		if userID := user.checkUser(db); userID != nil {
			switch userID {
			case sql.ErrNoRows:
				return "User Not Found", sql.ErrNoRows
			default:
				return "Something Went Wrong", err
			}
		}

		companyID, err := product.checkProduct(db)

		if err != nil {
			switch err {
			case sql.ErrNoRows:
				return "Product Not Found", sql.ErrNoRows
			default:
				return "Something Went Wrong", err
			}
		}

		insq := "INSERT INTO xlstore_productmention (user_id, product_id, mention, mention_date) "
		insq += "VALUES (?,?,?)"

		stmt, err := db.Prepare(insq)

		defer stmt.Close()

		if err != nil {
			return "Error While Preparing Statement", err
		}

		res, err := stmt.Exec(&mention.UserID, &mention.ProductID, &mention.Mention, &today)

		if err != nil {
			return "Error While Excecuting Statement", err
		}

		notq := "INSERT INTO xlstore_companynotifications (notification_id, concern_id, user_id, about, posted_date) "
		notq += "VALUES (?,?,?,?,?)"

		inserr := db.QueryRow(notq, &mention.ProductID, &companyID, &mention.UserID, &mention.Mention, &mention.MentionDate)

		if inserr != nil {
			return "Error While Inserting Notification", errors.New("Insertion Error")
		}

		mentionID, err := res.LastInsertId()

		if err != nil {
			return "Error While Getting Last Inserted ID", err
		}

		return strconv.FormatInt(mentionID, 10), nil
	}

	updateq := "UPDATE xlstore_productmention SET mention = ? WHERE id = ?"
	stmt, err := db.Prepare(updateq)

	defer stmt.Close()

	if err != nil {
		return "Error While Excecuting Statement", err
	}

	_, err = stmt.Exec(&mention.Mention, &response)

	if err != nil {
		return "Error When Updating Mention", err
	}

	return response, nil
}

func (product *Product) mGetProductComments(db *sql.DB) ([]Comment, error) {

	comments := []Comment{}
	q := "SELECT id, user_id, company_id, commenter, comment, comment_date FROM xlstore_productcomments WHERE product_id = ? ORDER BY comment_date DESC"
	rows, err := db.Query(q, &product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {

		var comment Comment
		if err := rows.Scan(
			&comment.ID,
			&comment.UserID,
			&comment.CompanyID,
			&comment.Commenter,
			&comment.Comment,
			&comment.CommentDate,
		); err != nil {
			return nil, err
		}

		if comment.Commenter == "user" {

			value, err := comment.UserID.Value()
			if err != nil {
				log.Fatal(err)
			}
			userID, err := strconv.Atoi(fmt.Sprintf("%d", value))

			if err != nil {
				log.Fatal(err)
			}

			user := User{Token: int64(userID)}
			if err := user.mGetUserProfile(db); err != nil {
				log.Fatal(err)
			}
			comment.User = user
			comments = append(comments, comment)

		} else {

			value, err := comment.CompanyID.Value()
			if err != nil {
				log.Fatal(err)
			}

			companyID, err := strconv.Atoi(fmt.Sprintf("%d", value))

			if err != nil {
				log.Fatal(err)
			}

			company := Company{ID: int64(companyID)}
			if err := company.mGetCompanyProfile(db); err != nil {
				log.Fatal(err)
			}
			comment.Company = company
			comments = append(comments, comment)

		}
	}

	return comments, nil
}

func (comment *Comment) mProductAddComment(db *sql.DB) (string, error) {

	product := Product{ID: comment.ProductID}
	commenter := "user"
	value, err := comment.UserID.Value()
	today := time.Now().UTC()

	if err != nil {
		log.Fatal(err)
	}

	userID, err := strconv.Atoi(fmt.Sprintf("%d", value))
	user := User{Token: int64(userID)}

	if err != nil {
		log.Fatal(err)
	}

	if err := user.checkUser(db); err != nil {
		switch err {
		case sql.ErrNoRows:
			return "User Not Found", sql.ErrNoRows
		default:
			return "Something Went Wrong", err
		}
	}

	companyID, err := product.checkProduct(db)

	if err != nil {
		switch err {
		case sql.ErrNoRows:
			return "Product Not Found", sql.ErrNoRows
		default:
			return "Something Went Wrong", err
		}
	}

	insq := "INSERT INTO xlstore_productcomments (user_id, product_id, commenter, comment, comment_date)"
	stmt, err := db.Prepare(insq)

	defer stmt.Close()

	if err != nil {
		return "Error While Preparing Statement", err
	}

	res, err := stmt.Exec(&comment.UserID, &comment.ProductID, &commenter, &comment.Comment, &today)

	if err != nil {
		return "Error While Excecuting Stattement", err
	}

	notq := "INSERT INTO xlstore_companynotifications (notification_id, concern_id, user_id, about, posted_date) "
	notq += "VALUES (?,?,?,?,?)"

	about := "comment"

	inserr := db.QueryRow(notq, &comment.ProductID, &companyID, &comment.UserID, &about, &today)

	if inserr != nil {
		return "Error While Inserting Notification", errors.New("Insertion Error")
	}

	commentID, err := res.LastInsertId()
	if err != nil {
		return "Error While Getting The Last ID", err
	}

	return strconv.FormatInt(commentID, 10), nil
}

func (comment *Comment) mProductUpdateComment(db *sql.DB) (string, error) {

	var userID int64
	checkq := "SELECT user_id FROM xlstore_productcomments WHERE id = ?"
	err := db.QueryRow(checkq, comment.ID).Scan(&userID)

	if err != nil {
		return "Comment Not Found", err
	}

	value, err := comment.UserID.Value()
	if err != nil {
		log.Fatal(err)
	}

	user, err := strconv.Atoi(fmt.Sprintf("%d", value))
	if err != nil {
		log.Fatal(err)
	}

	if int64(user) != userID {
		return "You are not the owner !!!", errors.New("Not Owner")
	}

	updateq := "UPDATE xlstore_productcomments SET comment = ? WHERE id = ?"
	_, err = db.Exec(updateq, comment.Comment, comment.ID)

	if err != nil {
		return "Error While Saving Comment Updates", nil
	}

	return "Comment Updated Successfully !!!", nil
}

func (comment *Comment) mProductDeleteComment(db *sql.DB) (string, error) {

	var userID int64
	checkq := "SELECT user_id FROM xlstore_productcomments WHERE id = ?"
	err := db.QueryRow(checkq, comment.ID).Scan(&userID)

	if err != nil {
		return "Comment Not Found", sql.ErrNoRows
	}

	value, err := comment.UserID.Value()
	if err != nil {
		log.Fatal(err)
	}

	user, err := strconv.Atoi(fmt.Sprintf("%d", value))
	if err != nil {
		log.Fatal(err)
	}

	if int64(user) != userID {
		return "You are not the owner !!!", errors.New("Not Owner")
	}

	deleteq := "DELETE FROM xlstore_productcomments WHERE id = ?"
	_, err = db.Exec(deleteq, comment.ID)

	if err != nil {
		return "Error While Deleting Comment", err
	}

	return "Comment Deleted Successfully !!!", nil
}

//Product Attributes Function

func (product *Product) getProductAdvertisment(db *sql.DB) []Advertisments {

	advertisments := []Advertisments{}
	q := "SELECT id, advertisment_text, video, posted_date FROM xlstore_advertisments WHERE product_id = ?"
	rows, err := db.Query(q, product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		var advertisment Advertisments

		if err := rows.Scan(
			&advertisment.ID,
			&advertisment.Description,
			&advertisment.VideoURL,
			&advertisment.PostedDate,
		); err != nil {
			log.Fatal(err)
		}

		advertisments = append(advertisments, advertisment)
	}

	return advertisments
}

func (product *Product) getProductPictures(db *sql.DB) []OtherImages {

	images := []OtherImages{}
	q := "SELECT image FROM xlstore_productpictures WHERE product_id = ?"
	rows, err := db.Query(q, product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		var image OtherImages
		if err := rows.Scan(&image.ImageURL); err != nil {
			log.Fatal(err)
		}
		images = append(images, image)
	}
	return images
}

func (product *Product) getProductSumInteress(db *sql.DB) (interess int64) {

	q := "SELECT * FROM xlstore_productinteress WHERE product_id = ?"
	rows, err := db.Query(q, product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		interess++
	}

	return interess
}

func (product *Product) getProductSumComments(db *sql.DB) (comments int64) {

	q := "SELECT * FROM xlstore_productcomments WHERE product_id = ?"
	rows, err := db.Query(q, product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		comments++
	}

	return comments
}

func (product *Product) getProductSumLikes(db *sql.DB) (likes int64) {

	q := "SELECT * FROM xlstore_productmention WHERE product_id = ? AND mention = 'like'"
	rows, err := db.Query(q, product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		likes++
	}

	return likes
}

func (product *Product) getProductSumDislikes(db *sql.DB) (dislikes int64) {

	q := "SELECT * FROM xlstore_productmention WHERE product_id = ? AND mention = 'dislike'"
	rows, err := db.Query(q, product.ID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {
		dislikes++
	}

	return dislikes
}

func (mention *Mention) getProductMentions(db *sql.DB) []Mention {

	mentions := []Mention{}
	q := "SELECT user_id, product_id, mention, mention_date FROM xlstore_productmention WHERE product_id = ?"

	rows, err := db.Query(q, &mention.ProductID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {

		var ment Mention
		if err := rows.Scan(&ment.UserID, &ment.ProductID, &ment.Mention, &ment.MentionDate); err != nil {
			log.Fatal(err)
		}

		mentions = append(mentions, ment)
	}

	return mentions
}

func (interess *Interess) getProductInterests(db *sql.DB) []Interess {

	interesses := []Interess{}
	q := "SELECT user_id, product_id, interess_date FROM xlstore_productinteress WHERE product_id = ?"

	rows, err := db.Query(q, &interess.ProductID)

	if err != nil {
		log.Fatal(err)
	}

	for rows.Next() {

		var interest Interess
		if err := rows.Scan(&interest.UserID, &interest.ProductID, &interest.InteressDate); err != nil {
			log.Fatal(err)
		}

		interesses = append(interesses, interest)
	}

	return interesses
}
