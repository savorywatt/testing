package chanbuff

import "testing"

type ShardTest struct {
	NumberData int
	DataSize   int
	Expected   int
}

var tests = []ShardTest{
	ShardTest{10, 100, 1},
	ShardTest{800, 100, 2},
	ShardTest{90, 10000, 2},
	ShardTest{90, 10000, 2},
	ShardTest{8100, 100, 17},
}

func TestMakeRequestsLock(t *testing.T) {

	for _, test := range tests {

		data := genData(test.NumberData, test.DataSize)

		result := MakeRequestsLock(data)

		if len(result) != test.Expected {
			t.Error("For", test.NumberData,
				"Expected", test.Expected,
				"Got", len(result),
				"Size", test.DataSize)
		}

	}
}

func genData(amount int, size int) []Data {
	var data []Data

	for i := 0; i <= amount; i++ {
		bytes := make([]byte, size)
		datum := Data{bytes}
		data = append(data, datum)
	}

	return data

}

func BenchmarkLock(b *testing.B) {
	data := genData(1000, 100)

	for i := 0; i < b.N; i++ {

		SendDataLock(data)
	}
}
