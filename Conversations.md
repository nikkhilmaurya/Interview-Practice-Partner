# SDE Mock Interview – Conversation Transcript

**Role Selected:** Software Development Engineer (SDE)  
**Mode:** Text-based mock interview  

---

**Interviewer:** Let's begin. Tell me about yourself.  

**You:** My name is Nikhil I am currently pursuing B.Tech in CSE. I have a strong foundation in DSA, C++ and OOPS concepts.  

---

**Interviewer:** Thanks for the introduction, Nikhil. Can you tell me about the most technically challenging project you've worked on, either academically or personally?  

**You:** I have worked upon one academic project which includes a snake game developed using C++.  

---

**Interviewer:** Okay, a classic C++ project. What was the most technically complex part of building the snake game?  

**You:** The most complex part was implementing real-time movement and collision detection. I handled the snake’s body using a linked list and managed continuous updates without screen flickering, which strengthened my understanding of pointers and memory management in C++.  

---

**Interviewer:** Interesting, you chose a linked list for the snake's body. Why was that a better fit for this problem than, for example, a dynamic array or a deque?  

**You:** A linked list was a better fit because the snake grows and shrinks frequently, and linked lists allow efficient insertion and deletion at the head and tail in O(1) time. With a dynamic array or deque, resizing or shifting elements would be more costly and less efficient for continuous gameplay.  

---

**Interviewer:** That makes sense regarding the insertion and deletion performance. Thinking about performance more broadly, how does using a linked list, with nodes potentially scattered in memory, affect the performance of rendering the snake on screen each frame compared to a contiguous data structure?  

**You:** Linked lists have poorer cache locality since nodes aren’t stored contiguously, so accessing them is slower than iterating through a contiguous array. This can slightly impact rendering performance, but for a small snake game the overhead is negligible.  

---

**Interviewer:** That's a great point about cache locality being a classic trade-off. Since you were managing the linked list nodes yourself in C++, how did you specifically handle their memory allocation and deallocation to prevent issues like memory leaks?  

**You:** I used dynamic allocation with `new` for each node and ensured proper cleanup using `delete` when removing segments. I kept deletion centralized in a function so every removed node was freed immediately, preventing leaks.  

---

**Interviewer:** Right, centralizing the deletion logic is a good practice for manual memory management. What would happen in your game if an exception were to be thrown after you've allocated a new node with `new` but before you've had a chance to call `delete` on it later?  

**You:** If an exception occurred, that allocated memory could be leaked because `delete` might never execute. Using RAII or smart pointers like `unique_ptr` would prevent that, since they automatically release memory even if exceptions happen.  

---

**Interviewer:** That's a very good point about RAII and smart pointers. You mentioned `unique_ptr` specifically—what exactly does "unique ownership" mean in the context of memory management?  

**You:** Unique ownership means only one `unique_ptr` can own a resource at a time. It can’t be copied—only moved—so there’s always a single clear owner responsible for deleting the memory automatically.  

---

**Interviewer:** That's a good summary of unique ownership. Can you describe a scenario where `unique_ptr` would be an inappropriate choice for managing an object's lifetime, and what you might use instead?  

**You:** `unique_ptr` is inappropriate when multiple parts of the program need shared ownership of the same object—like shared game resources or reference-counted objects. In that case, `shared_ptr` is more suitable.  

---

**Interviewer:** That's a great distinction to make. So in that context, what is a `weak_ptr` and in what kind of design situation would it be necessary?  

**You:** `weak_ptr` is a non-owning reference to an object managed by `shared_ptr`. It’s used to break cyclic references—for example in parent–child tree structures—so objects can be freed properly without reference-count loops.  

---

**Interviewer:** That's exactly the primary use case for `weak_ptr`. Let's stick with that parent–child tree example: if a parent node holds `shared_ptr`s to its children, and each child holds a `shared_ptr` back to its parent, what specifically prevents the memory from being deallocated when an external pointer to the root of that tree goes out of scope?  

**You:** The memory won’t be deallocated because both parent and child still hold `shared_ptr`s to each other, keeping the reference count above zero. This creates a circular reference so neither object gets destroyed. Replacing the child’s pointer back to the parent with a `weak_ptr` breaks the cycle since it doesn’t increase the reference count, allowing proper cleanup.

---

# ⭐ Candidate Evaluation

**Overall Score:** 9/10  
**Decision:** Strong Hire  

### **Strengths**
- Excellent clarity and depth on modern C++ memory management
- Demonstrated strong understanding of DSA and performance trade-offs
- Communicated clearly with real examples and reasoning
- Discussed RAII, unique/shared/weak pointers with correct scenarios

### **Areas to Improve**
- Slight improvement needed in opening introduction (more structured pitch)
- Could showcase a second major project for breadth

### **Recommendation**
Continue practicing behavioral questions and build another system-level project such as multithreading or networking.

---

**End of Interview Transcript**
