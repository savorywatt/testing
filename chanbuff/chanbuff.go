package chanbuff

import (
	"fmt"
	"strconv"
	"sync"
)

type Data struct {
	bytes []byte
}

type Message struct {
	bytes []byte
}

type MessageRequest struct {
	messages []*Message
}

// Take data
// Turn it into messages based on shard
//

const MaxBytes = 800
const MaxMessages = 500

func SendDataChannel(data []Data) {

	requests := make(chan *MessageRequest)
	done := make(chan bool)

	requestPool := sync.Pool{
		New: func() interface{} {
			return NewMessageRequest()
		},
	}

	messagePool := sync.Pool{
		New: func() interface{} {
			return NewMessage()
		},
	}

	go func() {

		count := 0
		for {

			request, more := <-requests

			if more {
				request.Deliver()

				fmt.Println("Messages", len(request.messages))
				for _, message := range request.messages {
					messagePool.Put(message)
					count += 1
				}
				requestPool.Put(request)

			} else {
				fmt.Println("Sent Messages:", strconv.Itoa(count))
				done <- true
			}
		}
	}()

	byteSize := 0
	messageCount := 0
	group := make([]*Message, 0)

	fmt.Println("Entities:", len(data))

	for _, entity := range data {

		//		message := &Message{entity.Payload()}
		message := messagePool.Get().(*Message)
		message.bytes = entity.Payload()
		length := len(message.bytes)

		if byteSize == 0 {

			group = append(group, message)
			messageCount += 1
			byteSize = length
		}

		if byteSize > MaxBytes*1024 || messageCount > MaxMessages {

			request := requestPool.Get().(*MessageRequest)

			request.messages = group
			requests <- request
			//			requests <- &MessageRequest{group}

			group = group[:0]
			group = append(group, message)
			messageCount = 1
			byteSize = length
		}

		group = append(group, message)
		messageCount += 1
		byteSize += length

	}

	requests <- &MessageRequest{group}
	close(requests)
}

func SendDataLock(data []Data) {

	requests := MakeRequestsLock(data)
	var groupLock sync.WaitGroup
	groupLock.Add(len(requests))

	for _, request := range requests {

		go func(r *MessageRequest) {

			r.Deliver()
			groupLock.Done()

		}(request)

	}

	groupLock.Wait()

}

func MakeRequestsLock(data []Data) []*MessageRequest {

	requests := make([]*MessageRequest, 0, len(data)/5)

	byteSize := 0
	messageCount := 0
	group := make([]*Message, 0)
	for _, entity := range data {

		message := &Message{entity.Payload()}
		length := len(message.bytes)

		if byteSize == 0 {

			group = append(group, message)

			messageCount += 1
			byteSize = length
		}

		if byteSize+length > MaxBytes*1024 || messageCount > MaxMessages {
			var request = &MessageRequest{group}
			requests = append(requests, request)

			group = group[:0]
			group = append(group, message)
			messageCount = 1
			byteSize = length

		}

		group = append(group, message)
		messageCount += 1
		byteSize += length

	}
	//	fmt.Println("final size", byteSize, "count", messageCount)

	var request = &MessageRequest{group}
	requests = append(requests, request)

	return requests
}

func (self *Data) Payload() []byte {

	return self.bytes
}

func (self *MessageRequest) Deliver() {

}

func NewMessageRequest() *MessageRequest {

	return &MessageRequest{}

}

func NewMessage() *Message {

	return &Message{}

}
