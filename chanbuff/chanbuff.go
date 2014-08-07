package chanbuff

import "sync"

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

		if byteSize > MaxBytes*1024 || messageCount > MaxMessages {
			//fmt.Println("other size", byteSize, "count", messageCount)
			var request = &MessageRequest{group}
			requests = append(requests, request)
			group = append(group, message)
			messageCount = 0
			byteSize = 0
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
