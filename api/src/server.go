package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"sync"
	"time"
	httptrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/net/http"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

type Bookmark struct {
	ID  string `json:"id"`
	URL string `json:"url"`
}

type apiHandler struct {
	sync.Mutex
	store map[string]Bookmark
}

func (h *apiHandler) bookmarks(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		h.get(w, r)
		return
	case "POST":
		h.post(w, r)
		return
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
}

func (h *apiHandler) get(w http.ResponseWriter, r *http.Request) {
	bookmarks := make([]Bookmark, len(h.store))
	h.Lock()
	i := 0
	for _, bookmark := range h.store {
		bookmarks[i] = bookmark
		i++
	}
	h.Unlock()

	jsonBytes, err := json.Marshal(bookmarks)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))
	}

	w.Header().Add("content-type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonBytes)
}

func (h *apiHandler) post(w http.ResponseWriter, r *http.Request) {
	bodyBytes, err := ioutil.ReadAll(r.Body)
	defer r.Body.Close()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))
		return
	}

	contentType := r.Header.Get("content-type")
	if contentType != "application/json" {
		w.WriteHeader(http.StatusUnsupportedMediaType)
		return
	}

	var bookmark Bookmark
	err = json.Unmarshal(bodyBytes, &bookmark)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(err.Error()))
		return
	}
	bookmark.ID = fmt.Sprintf("%d", time.Now().UnixNano())
	h.Lock()
	h.store[bookmark.ID] = bookmark
	defer h.Unlock()
}

func newAPIHandler() *apiHandler {
	return &apiHandler{
		store: map[string]Bookmark{},
	}
}

func main() {
	tracer.Start(tracer.WithDebugMode(true))
	defer tracer.Stop()
	mux := httptrace.NewServeMux()
	apiHandler := newAPIHandler()

	mux.HandleFunc("/api", apiHandler.bookmarks)
	
	err := http.ListenAndServe(":8080", mux)
	if err != nil {
		panic(err)
	}
}
