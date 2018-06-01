package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
)

type XlstoreAPI struct {
	Router *mux.Router
	DB     *sql.DB
}

//Initialize initializes XlstoreAPI struct
func (api *XlstoreAPI) Initialize() {

	var err error
	api.DB, err = sql.Open("mysql", "root:@tcp(127.0.0.1:3306)/xlstoredb")

	if err != nil {
		log.Fatal(err)
	}

	api.Router = mux.NewRouter().PathPrefix("/api").Subrouter()
	api.InitRoutes()
}

//Run runs the server
func (api *XlstoreAPI) Run() {
	http.ListenAndServe(":8800", api.Router)
}

//InitRoutes returns all urls
func (api *XlstoreAPI) InitRoutes() {

	//Users Routes

	api.Router.HandleFunc("/user/all/", api.getUsers).Methods("GET")
	api.Router.HandleFunc("/user/{token}/", api.getUserProfile).Methods("GET")
	api.Router.HandleFunc("/user/signup/", api.registerUser).Methods("POST")
	api.Router.HandleFunc("/user/authenticate/", api.userAuthencication).Methods("POST")

	//Company Routes

	api.Router.HandleFunc("/company/all/", api.getCompanies).Methods("GET")
	api.Router.HandleFunc("/company/{id}/", api.getCompanyProfile).Methods("GET")

	//Product Routes

	api.Router.HandleFunc("/product/all/", api.getProducts).Methods("GET")
	api.Router.HandleFunc("/product/{id}/", api.getSingleProduct).Methods("GET")
	api.Router.HandleFunc("/product/{id}/interess/", api.interessProduct).Methods("POST")
	api.Router.HandleFunc("/product/{id}/mention/", api.mentionProduct).Methods("POST")
	api.Router.HandleFunc("/product/{id}/comments/all/", api.getProductComments).Methods("GET")
	api.Router.HandleFunc("/product/{id}/comments/add/", api.addProductComment).Methods("POST")
	api.Router.HandleFunc("/product/{id}/comments/{comment}/update/", api.updateProductComment).Methods("POST")
	api.Router.HandleFunc("/product/{id}/comments/{comment}/delete/", api.deleteProductComment).Methods("POST")
}

//Users URLs Functions

func (api *XlstoreAPI) getUsers(w http.ResponseWriter, r *http.Request) {

	var user User
	users, err := user.mGetUsers(api.DB)

	if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, users)
}

func (api *XlstoreAPI) getUserProfile(w http.ResponseWriter, r *http.Request) {

	var user User
	vars := mux.Vars(r)
	token, err := strconv.Atoi(vars["token"])

	if err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid User Token")
		return
	}

	user = User{Token: int64(token)}

	if err := user.mGetUserProfile(api.DB); err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithMessage(w, http.StatusNotFound, "User Not Found")
		default:
			respondWithMessage(w, http.StatusInternalServerError, err.Error())
		}
		return
	}
	respondWithJSON(w, http.StatusOK, user)
}

func (api *XlstoreAPI) registerUser(w http.ResponseWriter, r *http.Request) {

	var user User
	decoder := json.NewDecoder(r.Body)

	if err := decoder.Decode(&user); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	token, err := user.mRegisterUser(api.DB)

	if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	user = User{Token: token}

	if err := user.mGetUserProfile(api.DB); err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithMessage(w, http.StatusNotFound, "User Not Found")
		default:
			respondWithMessage(w, http.StatusInternalServerError, err.Error())
		}
		return
	}

	respondWithJSON(w, http.StatusOK, user)
}

func (api *XlstoreAPI) userAuthencication(w http.ResponseWriter, r *http.Request) {

	var user UserAuthentication
	decoder := json.NewDecoder(r.Body)

	if err := decoder.Decode(&user); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	err := user.mUserAuthentication(api.DB)

	if err == sql.ErrNoRows {
		respondWithMessage(w, http.StatusNotFound, "Incorrect Email or Password")
		return
	}

	profile := User{Email: user.Email}

	if err := profile.mGetUserProfile(api.DB); err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithMessage(w, http.StatusNotFound, "User Not Found")
		default:
			respondWithMessage(w, http.StatusInternalServerError, err.Error())
		}
		return
	}

	respondWithJSON(w, http.StatusOK, profile)
}

//Company URLs Functions

func (api *XlstoreAPI) getCompanies(w http.ResponseWriter, r *http.Request) {

	var company Company
	companies, err := company.mGetCompanies(api.DB)

	if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}
	respondWithJSON(w, http.StatusOK, companies)
}

func (api *XlstoreAPI) getCompanyProfile(w http.ResponseWriter, r *http.Request) {

	var company Company
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])

	if err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Company ID")
	}

	company = Company{ID: int64(id)}

	if err := company.mGetCompanyProfile(api.DB); err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithMessage(w, http.StatusNotFound, "Company Not Found")
		default:
			respondWithMessage(w, http.StatusInternalServerError, err.Error())
		}
		return
	}
	respondWithJSON(w, http.StatusOK, company)
}

//Product URLs Function

func (api *XlstoreAPI) getProducts(w http.ResponseWriter, r *http.Request) {

	var product Product
	products, err := product.mGetProducts(api.DB)

	if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}
	respondWithJSON(w, http.StatusOK, products)
}

func (api *XlstoreAPI) getSingleProduct(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)
	productID, err := strconv.Atoi(vars["id"])

	if err != nil {
		log.Fatal(err)
	}

	product := Product{ID: int64(productID)}

	if err := product.mGetSingleProduct(api.DB); err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithMessage(w, http.StatusNotFound, "Product Not Found")
		default:
			respondWithMessage(w, http.StatusInternalServerError, err.Error())
		}
		return
	}
	respondWithJSON(w, http.StatusOK, product)
}

func (api *XlstoreAPI) interessProduct(w http.ResponseWriter, r *http.Request) {

	var interess Interess
	decoder := json.NewDecoder(r.Body)

	if err := decoder.Decode(&interess); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	response, err := interess.mInteressProduct(api.DB)

	if err == sql.ErrNoRows {
		respondWithMessage(w, http.StatusNotFound, response)
		return
	} else if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithMessage(w, http.StatusOK, response)
}

func (api *XlstoreAPI) mentionProduct(w http.ResponseWriter, r *http.Request) {

	var mention Mention
	decoder := json.NewDecoder(r.Body)

	if err := decoder.Decode(&mention); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	response, err := mention.mMentionProduct(api.DB)

	if err == sql.ErrNoRows {
		respondWithMessage(w, http.StatusNotFound, response)
		return
	} else if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithMessage(w, http.StatusOK, response)
}

func (api *XlstoreAPI) getProductComments(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)
	productID, err := strconv.Atoi(vars["id"])

	if err != nil {
		log.Fatal(err)
	}

	product := Product{ID: int64(productID)}
	_, err = product.checkProduct(api.DB)

	if err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithMessage(w, http.StatusNotFound, "Product Not Found")
			return
		default:
			respondWithMessage(w, http.StatusInternalServerError, err.Error())
			return
		}
	}

	comments, err := product.mGetProductComments(api.DB)

	if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, comments)
}

func (api *XlstoreAPI) addProductComment(w http.ResponseWriter, r *http.Request) {

	var comment Comment
	decode := json.NewDecoder(r.Body)

	if err := decode.Decode(&comment); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	response, err := comment.mProductAddComment(api.DB)

	if err == sql.ErrNoRows {
		respondWithMessage(w, http.StatusNotFound, response)
		return
	} else if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithMessage(w, http.StatusOK, response)
}

func (api *XlstoreAPI) updateProductComment(w http.ResponseWriter, r *http.Request) {

	var comment Comment
	decode := json.NewDecoder(r.Body)

	if err := decode.Decode(&comment); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	response, err := comment.mProductUpdateComment(api.DB)

	if err != nil {
		respondWithJSON(w, http.StatusInternalServerError, err.Error())
	}

	respondWithMessage(w, http.StatusOK, response)
}

func (api *XlstoreAPI) deleteProductComment(w http.ResponseWriter, r *http.Request) {

	var comment Comment
	decode := json.NewDecoder(r.Body)

	if err := decode.Decode(&comment); err != nil {
		respondWithMessage(w, http.StatusBadRequest, "Invalid Request Data")
		return
	}

	defer r.Body.Close()

	response, err := comment.mProductDeleteComment(api.DB)

	if err == sql.ErrNoRows {
		respondWithMessage(w, http.StatusNotFound, response)
		return
	} else if err != nil {
		respondWithMessage(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithMessage(w, http.StatusOK, response)
}

func main() {
	api := XlstoreAPI{}
	api.Initialize()
	api.Run()
}
