package main

import (
	"encoding/json"
	"net/http"
	"strconv"
)

func respondWithMessage(w http.ResponseWriter, code int, message string) {
	respondWithJSON(w, code, map[string]string{"status": strconv.FormatUint(uint64(code), 10), "message": message})
}

func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	response, _ := json.Marshal(payload)

	setHeaders(w)
	w.WriteHeader(code)
	w.Write(response)
}

func setHeaders(w http.ResponseWriter) {
	w.Header().Add("Content-Type", "application/json")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Access-Control-Allow-Headers", "origin, x-requested-with, content-type")
}
