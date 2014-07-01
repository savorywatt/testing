package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

type Video struct {
	Filename string
	Data     []byte
}

func loadFile(filename string) (*Video, error) {

	data, err := ioutil.ReadFile(filename)

	if err != nil {
		return nil, err
	}

	return &Video{Filename: filename, Data: data}, nil
}

func handler(w http.ResponseWriter, r *http.Request) {

	fmt.Fprintf(w, "Nothing to see")
}

type rangeTuple struct {
	start, end int64
}

func parseRange(rangeReq string) []rangeTuple {

	const bytes = "bytes="
	if !strings.Contains(rangeReq, bytes) {
		return nil, errors.new("invalid range")
	}

	for _, value := range strings.split(rangeReq[len(bytes):], ",") {

		value := strings.TrimSpace(value)

	}

}

func videoHandler(w http.ResponseWriter, r *http.Request) {

	filename := r.URL.Path[len("/video/"):]

	// extract range of bytes to send back
	rangeReq := r.Header.Get("Range")
	ranges := parseRange(rangeReq)

}
