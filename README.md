# Django-Library-Management



### 0.15

+ Since there is a lot of authors and genres out there, the MultipleChoiceField was generally a bad option since it loaded thousands of values. I modified manager and form so now it uses TextField and comma separated string to add or modify associated ManyToMany objects.

### 0.22

+ Added better script for loading csv file to database. Now it runs in 2 minutes instead of 50 to load 100k records.

### 0.23

+ With 100k records, complex search with Q object turned out to be very slow at times. I changed the search method by adding separate views to search by title, author, or genre. It's much faster and more convinient for user.
+ Added BaseListView class, from which subclasses inherit get_queryset() and get_context_data() methods.
+ Added templates for author and genre views.
+ Wrote few unit tests to cover changes made in last time.

### 0.24

+ Added pre_delete signal to make book aviable for loan again, after order associated with the book has been deleted.

### 0.25

+ Added functional tests for /users/.