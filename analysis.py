


class ResumeAnalyzer:

    def generate_prompt(self, job_description, resume_text):
        """Generate the structured prompt with the job description and resume."""
        prompt = f"""
        Task:
            Analyze the provided resume text in relation to the job description and generate a comprehensive report with the following details:

            1. **Relevance Score**: A percentage (0-100%) indicating how closely the resume matches the job description.
            2. **Strengths**: Key areas where the resume aligns well with the job description and demonstrates suitable skills/experiences.
            3. **Weaknesses**: Areas where the resume lacks alignment with the job description or requires improvement.
            4. **Suggestions**: Actionable advice to improve the resume's alignment with the job description.
            5. **Keywords**: Missing or underrepresented keywords that are important for this job role.
            6. **Grammar and Writing Quality**: Evaluate grammar, tone, and writing quality. Point out errors, redundant phrases, and areas that can be rephrased for clarity.

            Output Format:

                Relevance Score: [XX%]
                Strengths: [List key areas of alignment (skills, experiences, etc.)]
                Weaknesses: [List areas requiring improvement or lacking alignment]
                Suggestions: [Provide actionable feedback, e.g., "Add experience in X to match the requirement for Y."]
                Keywords: [List missing/underused critical keywords]
                Grammar and Writing Quality:
                    Grammar Errors: [List specific errors with examples, e.g., "Incorrect verb tense in 'Managed projects that was successful.'"]
                    Clarity Issues: [Point out vague or unclear phrases, e.g., "Avoid repetitive phrasing like 'responsible for.'"]
                    Professional Tone: [Suggest improvements, e.g., "Use action verbs like 'spearheaded' instead of 'was involved in."]

            Additional Considerations:
                - Ensure feedback is actionable, clear, and professional.
                - Separate technical and soft skills alignment when necessary.
                - Provide examples or rewritten suggestions for grammar and clarity issues.
                - Tailor feedback to be constructive and supportive.
        response should be ats optimized
        Provide the response in JSON format.

        job_description = {job_description}
        resume_text = {resume_text}
        """
        return prompt
