// Updating the mentor schema to include CU field

const mentorSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    subject: { type: String, required: true },
    CU: { type: String, required: true }, // New CU field added
    // Other existing fields...
});

// Function to allocate mentors based on CU criteria
function allocateMentorBasedOnCU(mentors, cuCriteria) {
    return mentors.filter(mentor => mentor.CU === cuCriteria);
}

// Example allocation
const mentors = [ /* existing mentor objects */ ];
const allocatedMentors = allocateMentorBasedOnCU(mentors, 'CU-123'); // Replace with actual criteria