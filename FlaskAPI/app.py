from flask import Flask, request, jsonify

app = Flask(__name__)

students = [
    {'id': 1, 'name': 'Saniya', 'subject':'Math'},
    {'id': 2, 'name': 'Samarth', 'subject':'Science'},
    {'id': 3, 'name': 'Durva', 'subject':'Biology',}    
]
next_id=3
@app.route('/')
def home():
    return "Hello User"

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((student_id for student in students if student['id'] == student_id), None)
    if student_id:
        return jsonify(students)
    return jsonify({'message':'Identity not found'}),404

@app.route('/students',methods=['POST'])
def create_student():
    global next_id
    new_student_data = request.get_json()

    if not new_student_data or 'name' not in new_student_data or 'subject' not in new_student_data:
        return jsonify({'message': 'Invalid'}), 400

    new_student ={
        'id': next_id,
        'name': new_student_data['name'],
        'subject':new_student_data['subject'],
        
    }

    next_id+=1
    students.append(new_student)
    return jsonify(new_student),201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((student for student in students if student['id'] == student_id), None)
    if student:
        update_data=request.get_json()
        if 'name' in update_data:
            student['name']= update_data['name']
        if 'subject' in update_data:
            student['subject']= update_data['subject']
        return jsonify(student)
    return jsonify({'message': 'Identity not Found'}),404

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((student for student in students if student['id'] == student_id), None)
    if student:
        students = [i for i in students if i['id'] != student_id]
        return jsonify({'message': f'student {student_id} deleted'})
    return jsonify({'message': 'student not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)