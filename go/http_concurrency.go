package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"sync"
)

const (
	HttpStatusCodeOk = 200
)

var wg sync.WaitGroup
var ch chan int
var pool = sync.Pool{
	New: func() any {
		return new(string)
	},
}
var res []string

func ConcurrentRequest(parallelism int32, url string, reqBody [][]byte) {
	ch = make(chan int, parallelism)
	sumNum := len(reqBody)
	for i := 0; i < sumNum; i++ {
		ch <- i
		wg.Add(1)
		go doConcurrentRequest(i, url, reqBody[i])
	}
	wg.Wait()
}

func doConcurrentRequest(idx int, url string, reqBody []byte) {
	fmt.Printf("idx[%d]", idx)
	defer func() {
		<-ch
		wg.Done()
	}()
	var err error
	respBody := pool.Get().(*string)
	data, err := doPostRequest(url, reqBody)
	if err != nil {
		fmt.Printf("doPostRequest url[%s] req[%s] error[%s]", url, string(reqBody), err)
		return
	}
	res = append(res, data)
	pool.Put(respBody)
}

func doPostRequest(url string, reqBody []byte) (string, error) {
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(reqBody))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != HttpStatusCodeOk {
		fmt.Printf("status code[%d] header[%+v]", resp.StatusCode, resp.Header)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(body), nil
}

func main() {
	url := "https://apis.map.qq.com/bigdata/realtime/v1.1/population"
	var bodys [][]byte
	reqBody := []byte("{\"id\":\"11260\",\"begin\":1683216000,\"end\":1683298800,\"interval\":60,\"people_type\":\"all\",\"key\":\"RIJBZ-UMEYD-DN24N-PLYIV-ZVFKO-R4BBL\"}")
	for i := 0; i < 20; i++ {
		bodys = append(bodys, reqBody)
	}
	ConcurrentRequest(10, url, bodys)
	fmt.Printf("len[%d] res[%+v]", len(res), res)
}
