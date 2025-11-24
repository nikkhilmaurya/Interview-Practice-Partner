# Interview Practice – SDE Mock Interview Transcript

This document contains the transcript of a mock interview for the **Software Development Engineer (SDE)** role.  
The conversation demonstrates responses related to **Object-Oriented Programming (OOP)** principles and real project examples.
Model used in this is Gemini 2.5 flash

---

## 🎤 **Mock Interview Conversation**

### **Interviewer:** Let's begin. Tell me about yourself.  
**You:** My name is Nikhil, currently pursuing B.Tech in CSE. I have a strong foundation in DSA, C++, and OOPS concepts.

---

### **Interviewer:** Thanks for the introduction, Nikhil. Can you tell me about the most technically challenging project you've worked on in OOPS?  
**You:** I developed a Ride-Sharing App that demonstrated OOP concepts.

---

### **Interviewer:** Great. Tell me how you implemented polymorphism.  
**You:** By using runtime polymorphism through a `Vehicle` base class inherited by `Bike`, `Car`, and `Auto`, allowing dynamic fare calculation based on vehicle type.

---

### **Interviewer:** That's a clear example. Thinking about that `Vehicle` base class, what considerations did you have in designing shared vs. specific properties?  
**You:** Common attributes like `vehicleNumber`, `capacity`, and a generic `calculateFare()` were defined in the base class. Type-specific fare logic and additional charges were implemented in subclasses to keep the design flexible and extensible.

---

### **Interviewer:** When you designed the `calculateFare()` method, did you consider making it abstract? What would be the implications?  
**You:** Initially, I did not think deeply about abstract methods. I implemented `calculateFare()` directly in the base class and let subclasses override it.

---

### **Interviewer:** Could you explain what abstract methods are and when they might be beneficial?  
**You:** Abstract methods are methods without implementation. They are useful when the base class can’t define a general implementation, and child classes must provide specific behavior.

---

### **Interviewer:** How would making `calculateFare()` abstract affect the subclasses?  
**You:** It would force `Bike`, `Car`, and `Auto` to implement their own version, guaranteeing correctness and consistency.

---

### **Interviewer:** What would happen if `Bike` subclass forgot to implement the abstract method?  
**You:** The code would fail at compile time since all subclasses must implement abstract methods.

---

### **Interviewer:** From a design perspective, what advantage does that enforcement provide?  
**You:** It ensures that developers follow the required design rules early, reducing runtime issues and improving maintainability.

---

### **Interviewer:** Moving forward, did you consider using Java interfaces and what trade-offs exist vs. abstract classes?  
**You:** I used interfaces to define contract behavior. Interfaces define method signatures only, whereas abstract classes allow shared code and common attributes. Interfaces enable multiple inheritance while abstract classes do not.

---

### **Interviewer:** Thank you for your time. The interview is now complete.

---

## 📊 Final Evaluation

**Score:** 5 / 10  

### 🟢 Strengths
- Demonstrated understanding of polymorphism in a practical project
- Correctly recognized compile-time safety benefits
- Able to describe inheritance structure and real use case

### 🔧 Areas to Improve
- Needs deeper reasoning behind design decisions
- Should strengthen concepts of abstract classes vs interfaces with examples
- Expand justification for architectural choices

### 📚 Suggested Practice
- Redesign the Ride-Sharing App using both abstract classes and interfaces intentionally
- Write design notes explaining *why* each OOP feature was selected

---

## 🧠 Learning Outcome
This interview helps improve:
- Communication of technical decisions
- Depth of conceptual understanding of OOP
- Ability to justify design choices in an interview setting

---

### **End of Transcript**
