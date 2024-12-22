# Document Archive Portal (DA Portal)

## Technologies Used
Django, Django PasswordResetView, MySQL, AWS S3, HTML5, CSS3, Bootstrap5


## Problem Statement
In a financial institution, the process of loan and account opening approvals involves multiple steps, including document submission, review, approval, and rejection. The traditional method of handling these processes is often manual, time-consuming, and prone to errors. Additionally, storing documents for long-term retention securely and efficiently poses a significant challenge. The lack of automated notifications for different stages of the approval process leads to delays and communication gaps.


## Solution
The Document Archive Portal (DA Portal) is designed to streamline and automate the document submission and approval process. It addresses the following key areas:
1. **Document Submission and Storage:**
   - Users can easily upload documents required for loan and account opening approvals.
   - Documents are securely stored in an AWS S3 bucket, ensuring reliable and scalable long-term storage.

2. **Approval Workflow:**
   - The portal provides an intuitive interface for reviewers to approve or reject documents.
   - Each document's status is tracked, and the workflow is streamlined to reduce manual intervention and errors.

3. **Email Notifications:**
   - Automated email notifications are sent to users at different stages of the process:
     - When a document is uploaded.
     - When a document is approved.
     - When a document is rejected.
   - This ensures timely communication and reduces delays in the approval process.

4. **User Authentication and Password Management:**
   - Implemented Django's PasswordResetView for secure and efficient password management.
   - Ensures users can reset their passwords securely if forgotten.


## Implementation Details
- **Backend:**
  - Developed using Django, providing a robust and scalable backend framework.
  - Integrated MySQL for efficient and reliable database management.
  
- **Storage:**
  - Leveraged AWS S3 for secure, scalable, and cost-effective document storage.
  
- **Email Notifications:**
  - Configured Django to send automated email notifications using SMTP for various events (upload, approval, rejection).


## Impact
The DA Portal significantly improves the workflow within the organization by:
- Reducing the time taken to process loan and account opening applications.
- Minimizing errors associated with manual document handling.
- Enhancing communication through automated email notifications.
- Ensuring secure and reliable long-term storage of important documents.


## Conclusion
The Document Archive Portal (DA Portal) is a comprehensive solution that addresses the critical needs of the financial institution. By automating the document approval workflow and ensuring secure storage and timely communication, the portal enhances operational efficiency and improves user experience.
