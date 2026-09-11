# fallback / dummy data

hostel_blocks = [
  {
    "block_name": "A",
    "rooms": [
      {
        "room_name": "A1",
        "capacity": 3, # total number of students that can live
        "occupants": 1, # current number of students in the room
        "rate": 10000 # amount payable by each student in the room
      },
      {
        "room_name": "A2",
        "capacity": 3,
        "occupants": 0,
        "rate": 10000
      },
    ]
  },
  {
    "block_name": "B",
    "rooms": [
      {
        "room_name": "B1",
        "capacity": 4,
        "occupants": 1,
        "rate": 15000
      },
      {
        "room_name": "B2",
        "capacity": 4,
        "occupants": 0,
        "rate": 15000
      },
    ]
  },
  {
    "block_name": "C",
    "rooms": [
      {
        "room_name": "C1",
        "capacity": 5,
        "occupants": 0,
        "rate": 20000
      },
      {
        "room_name": "C2",
        "capacity": 5,
        "occupants": 0,
        "rate": 20000
      },
    ]
  },
]

students = [
  {
    "name": "Mary",
    "reg_no": "VU001",
    "block_name": "A",
    "room_name": "A1",
    "balance": 5000,
  },
  {
    "name": "John",
    "reg_no": "VU002",
    "block_name": "B",
    "room_name": "B1",
    "balance": 10000,
  },
]

# List to record fee payment transactions
payments = [
  {
    "reg_no": "VU001",
    "name": "Mary",
    "amount": 5000,
    "date": "2026-09-01"
  },
  {
    "reg_no": "VU002",
    "name": "John",
    "amount": 5000,
    "date": "2026-09-01"
  }
]



