from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker

from accounts.models import User
from ai_literacy.models import AILiteracyFramework, LearningModule, StudentProgress
from assessments.models import ReadinessQuestionnaire, Question, QuestionOption, AssessmentAttempt, StudentResponse
from curriculum.models import CurriculumIntegration, Assignment, AssignmentSubmission
from inclusivity.models import InterventionProgram, MentorshipProgram, MentorshipEnrollment, SupportResource
from ethics.models import EthicalCaseStudy, DiscussionForum, DiscussionPost, EthicalPrinciple

fake = Faker()

# Real AI literacy content data
AI_MODULES_CONTENT = {
    'What is Artificial Intelligence?': """
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving.

Key Concepts:
- AI systems can perform tasks that typically require human intelligence
- Machine learning allows systems to improve from experience
- Neural networks mimic the human brain's structure
- AI can be narrow (specific tasks) or general (human-like intelligence)

Applications in real world include virtual assistants, recommendation systems, autonomous vehicles, and medical diagnosis tools.

Historical Context:
The term "artificial intelligence" was coined in 1956 at the Dartmouth Conference. Since then, AI has evolved through multiple waves of development, from rule-based systems to modern deep learning approaches.

Future Implications:
AI is expected to transform industries including healthcare, finance, education, and transportation. Understanding AI fundamentals is crucial for professionals across all disciplines.
    """,
    
    'Machine Learning Fundamentals': """
Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves.

Types of Machine Learning:
1. Supervised Learning - Learning from labeled data (e.g., email spam detection)
2. Unsupervised Learning - Finding patterns in unlabeled data (e.g., customer segmentation)
3. Reinforcement Learning - Learning through trial and error (e.g., game playing AI)

Common Algorithms:
- Decision Trees: Tree-like models for classification and regression
- Random Forests: Ensemble of decision trees for improved accuracy
- Support Vector Machines: Finding optimal hyperplanes for classification
- Gradient Boosting: Sequential ensemble method for prediction tasks

Real-World Applications:
- Netflix recommendation system
- Credit card fraud detection
- Medical diagnosis assistance
- Stock market prediction
- Natural language processing

Key Terminology:
- Features: Input variables used for predictions
- Labels: Output variables (in supervised learning)
- Training Set: Data used to train the model
- Test Set: Data used to evaluate model performance
- Overfitting: When model performs well on training data but poorly on new data
    """,
    
    'Neural Networks Basics': """
Neural networks are computing systems inspired by biological neural networks that constitute animal brains. They are a series of algorithms that endeavor to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates.

Architecture:
- Input Layer: Receives the initial data (features)
- Hidden Layers: Process and transform the data through weighted connections
- Output Layer: Produces the final prediction or classification

Key Components:
1. Neurons (Nodes): Basic processing units that receive, process, and transmit information
2. Weights: Parameters that determine the strength of connections between neurons
3. Biases: Additional parameters that help shift the activation function
4. Activation Functions: Non-linear functions that introduce complexity (ReLU, Sigmoid, Tanh)

Learning Process:
- Forward Propagation: Data flows from input to output
- Loss Calculation: Measuring prediction error
- Backpropagation: Adjusting weights to minimize error
- Gradient Descent: Optimization algorithm to find best weights

Types of Neural Networks:
- Feedforward Neural Networks: Basic architecture for general tasks
- Convolutional Neural Networks (CNN): Specialized for image processing
- Recurrent Neural Networks (RNN): Designed for sequential data
- Long Short-Term Memory (LSTM): Advanced RNN for long sequences

Applications:
- Image recognition and classification
- Speech recognition
- Language translation
- Autonomous driving
- Medical image analysis
    """,
    
    'Deep Learning Introduction': """
Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers (deep networks) to progressively extract higher-level features from raw input.

Why "Deep"?
The term refers to the number of layers in the neural network. Traditional neural networks had 2-3 layers, while deep networks can have dozens or even hundreds of layers.

Key Advantages:
- Automatic Feature Extraction: No need for manual feature engineering
- Scalability: Performance improves with more data
- Versatility: Applicable to diverse domains (vision, speech, text)
- State-of-the-art Results: Achieves best performance on many tasks

Popular Deep Learning Architectures:
1. ResNet (Residual Networks): Enables training of very deep networks
2. VGG: Simple but effective architecture for image classification
3. Inception: Efficient multi-scale feature extraction
4. Transformers: Revolutionary architecture for NLP tasks

Deep Learning Frameworks:
- TensorFlow: Google's comprehensive ML framework
- PyTorch: Facebook's flexible deep learning library
- Keras: High-level API for rapid prototyping
- JAX: High-performance numerical computing

Challenges:
- Requires large amounts of labeled data
- Computationally expensive (needs GPUs)
- Difficult to interpret (black box problem)
- Prone to overfitting without proper regularization

Practical Considerations:
- Data preprocessing and augmentation
- Choosing appropriate architecture
- Hyperparameter tuning
- Model evaluation and validation
- Deployment and inference optimization
    """,
    
    'Natural Language Processing': """
Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and manipulate human language. It bridges the gap between human communication and computer understanding.

Core NLP Tasks:
1. Text Classification: Categorizing text into predefined classes (spam detection, sentiment analysis)
2. Named Entity Recognition: Identifying entities like names, locations, organizations
3. Machine Translation: Converting text from one language to another
4. Question Answering: Providing answers to questions posed in natural language
5. Text Summarization: Creating concise summaries of longer documents
6. Speech Recognition: Converting spoken language to text

Key Techniques:
- Tokenization: Breaking text into words or subwords
- Lemmatization: Reducing words to their base form
- Part-of-Speech Tagging: Identifying grammatical roles
- Dependency Parsing: Analyzing grammatical structure
- Word Embeddings: Vector representations of words (Word2Vec, GloVe)

Modern Approaches:
- Transformer Models: Attention-based architecture for sequence processing
- BERT: Bidirectional encoder for language understanding
- GPT: Generative pre-trained transformer for text generation
- T5: Text-to-text transfer transformer

Real-World Applications:
- Virtual assistants (Siri, Alexa, Google Assistant)
- Chatbots and customer service automation
- Email filtering and categorization
- Social media sentiment analysis
- Document search and retrieval
- Content moderation
- Language learning applications

Challenges in NLP:
- Ambiguity in language
- Context understanding
- Handling multiple languages
- Dealing with sarcasm and idioms
- Cultural and regional variations
    """,
    
    'Computer Vision Basics': """
Computer Vision is a field of AI that enables computers to derive meaningful information from digital images, videos, and other visual inputs, and take actions or make recommendations based on that information.

Fundamental Tasks:
1. Image Classification: Categorizing entire images
2. Object Detection: Locating and classifying objects within images
3. Image Segmentation: Partitioning images into meaningful regions
4. Facial Recognition: Identifying individuals from facial features
5. Pose Estimation: Detecting human body positions and movements
6. Image Generation: Creating new images from scratch or modifying existing ones

Key Techniques:
- Convolutional Neural Networks (CNNs): Specialized for processing grid-like data
- Feature Detection: Identifying edges, corners, and textures
- Image Preprocessing: Normalization, augmentation, filtering
- Transfer Learning: Using pre-trained models for new tasks

Popular CNN Architectures:
- AlexNet: Pioneering deep CNN for image classification
- VGG: Deep network with simple architecture
- ResNet: Residual connections for very deep networks
- YOLO: Real-time object detection
- U-Net: Architecture for image segmentation

Applications:
- Medical imaging diagnosis (X-rays, MRIs, CT scans)
- Autonomous vehicles (obstacle detection, lane keeping)
- Facial recognition systems
- Manufacturing quality control
- Agricultural monitoring
- Augmented reality
- Security and surveillance

Advanced Topics:
- 3D Vision: Depth estimation and 3D reconstruction
- Video Analysis: Action recognition and tracking
- Generative Models: GANs for image synthesis
- Few-shot Learning: Learning from limited examples

Ethical Considerations:
- Privacy concerns in facial recognition
- Bias in training data
- Surveillance and civil liberties
- Deepfakes and misinformation
    """,
    
    'AI Ethics and Responsible AI': """
AI Ethics involves the moral principles and techniques that guide the development and deployment of artificial intelligence systems. As AI becomes more prevalent, understanding ethical implications is crucial.

Core Ethical Principles:
1. Fairness and Non-Discrimination: Ensuring AI systems treat all individuals equitably
2. Transparency and Explainability: Making AI decisions understandable
3. Privacy and Data Protection: Safeguarding personal information
4. Accountability: Establishing responsibility for AI decisions
5. Safety and Security: Preventing harm and misuse

Key Ethical Issues:
- Algorithmic Bias: Systematic errors favoring certain groups over others
- Job Displacement: Automation's impact on employment
- Privacy Invasion: Surveillance and data collection concerns
- Autonomous Weapons: Military applications of AI
- Deepfakes: Manipulated media and misinformation
- Environmental Impact: Energy consumption of large AI models

Fairness in AI:
- Demographic Parity: Equal outcomes across groups
- Equal Opportunity: Equal true positive rates
- Individual Fairness: Similar individuals treated similarly
- Bias Detection: Identifying unfair patterns in data and models
- Bias Mitigation: Techniques to reduce discriminatory outcomes

Transparency and Explainability:
- Interpretable Models: Using simpler, more understandable algorithms
- Feature Importance: Identifying which inputs matter most
- LIME and SHAP: Techniques for explaining individual predictions
- Documentation: Clearly communicating model capabilities and limitations

Privacy-Preserving AI:
- Differential Privacy: Adding noise to protect individual data
- Federated Learning: Training on distributed data without centralization
- Secure Multi-Party Computation: Collaborative learning without sharing data
- Homomorphic Encryption: Computing on encrypted data

Responsible AI Development:
- Diverse Development Teams: Including varied perspectives
- Stakeholder Engagement: Involving affected communities
- Impact Assessments: Evaluating potential harms
- Continuous Monitoring: Tracking performance and fairness over time
- Human Oversight: Maintaining human control over critical decisions

Regulatory Frameworks:
- GDPR: European data protection regulation
- AI Act: Proposed EU regulation for AI systems
- Algorithmic Accountability Acts: US legislative proposals
- Industry Self-Regulation: Company-specific ethical guidelines

Best Practices:
- Conduct algorithmic audits
- Establish ethics review boards
- Implement fairness metrics
- Provide opt-out mechanisms
- Ensure data quality and representativeness
- Document training data and model decisions
    """,
    
    'AI in Healthcare': """
Artificial Intelligence is revolutionizing healthcare through improved diagnostics, personalized treatment, drug discovery, and patient care management.

Medical Imaging:
- X-ray Analysis: Detecting fractures, tumors, and abnormalities
- MRI Interpretation: Identifying brain lesions and structural issues
- CT Scan Analysis: Diagnosing internal injuries and diseases
- Retinal Screening: Early detection of diabetic retinopathy
- Pathology: Analyzing tissue samples for cancer detection

Clinical Applications:
1. Diagnosis Support: AI assists doctors in identifying diseases
2. Treatment Planning: Personalized therapy recommendations
3. Predictive Analytics: Forecasting patient outcomes and risks
4. Clinical Documentation: Automated note-taking and coding
5. Virtual Health Assistants: Patient engagement and monitoring

Drug Discovery and Development:
- Molecular Design: Predicting drug candidates
- Clinical Trial Optimization: Patient selection and protocol design
- Adverse Effect Prediction: Identifying potential side effects
- Drug Repurposing: Finding new uses for existing medications

Genomics and Precision Medicine:
- Genome Sequencing Analysis: Identifying genetic variants
- Cancer Genomics: Personalized cancer treatment
- Pharmacogenomics: Predicting drug responses based on genetics
- Disease Risk Assessment: Genetic predisposition analysis

Remote Patient Monitoring:
- Wearable Devices: Continuous health tracking
- Chronic Disease Management: Diabetes, heart disease monitoring
- Early Warning Systems: Detecting deterioration before crises
- Telemedicine: AI-enhanced remote consultations

Benefits:
- Improved Diagnostic Accuracy: Reducing human error
- Faster Processing: Analyzing images and data quickly
- 24/7 Availability: Continuous monitoring and support
- Cost Reduction: More efficient resource utilization
- Personalization: Tailored treatment plans

Challenges:
- Data Privacy: Protecting sensitive health information
- Regulatory Approval: Meeting safety and efficacy standards
- Integration: Fitting into existing healthcare workflows
- Liability: Determining responsibility for AI errors
- Trust: Building confidence among patients and providers
- Bias: Ensuring fairness across diverse populations

Future Directions:
- AI-powered surgical robots
- Real-time clinical decision support
- Population health management
- Mental health applications
- Pandemic prediction and response
    """,
    
    'AI in Business and Finance': """
AI is transforming business operations, financial services, and decision-making processes across industries.

Business Intelligence and Analytics:
- Customer Behavior Analysis: Understanding purchasing patterns
- Market Trend Prediction: Forecasting demand and trends
- Sentiment Analysis: Gauging customer opinions from social media
- Competitive Intelligence: Monitoring competitor activities
- Sales Forecasting: Predicting future revenue

Financial Applications:
1. Algorithmic Trading: Automated buying and selling of securities
2. Credit Scoring: Assessing loan default risk
3. Fraud Detection: Identifying suspicious transactions
4. Risk Management: Evaluating portfolio risks
5. Customer Service: Chatbots for banking inquiries
6. Robo-Advisors: Automated investment management

Marketing and Customer Experience:
- Personalized Recommendations: Product suggestions based on behavior
- Dynamic Pricing: Adjusting prices based on demand
- Customer Segmentation: Identifying distinct customer groups
- Churn Prediction: Identifying customers likely to leave
- Ad Targeting: Optimizing advertising campaigns
- Content Generation: Creating marketing copy and images

Operations and Supply Chain:
- Demand Forecasting: Predicting inventory needs
- Route Optimization: Efficient logistics planning
- Quality Control: Automated defect detection
- Predictive Maintenance: Anticipating equipment failures
- Warehouse Automation: Robotic picking and packing

Human Resources:
- Resume Screening: Filtering job applications
- Candidate Matching: Finding best-fit candidates
- Employee Retention: Predicting turnover
- Performance Analysis: Evaluating employee productivity
- Training Recommendations: Personalized learning paths

Benefits to Business:
- Increased Efficiency: Automating repetitive tasks
- Better Decisions: Data-driven insights
- Cost Reduction: Optimizing resource allocation
- Enhanced Customer Experience: Personalization at scale
- Competitive Advantage: Faster innovation

Challenges:
- Implementation Costs: Initial investment requirements
- Data Quality: Ensuring accurate and complete data
- Change Management: Overcoming organizational resistance
- Skills Gap: Finding qualified AI talent
- Ethical Concerns: Bias in hiring, lending decisions

Case Studies:
- Netflix: Recommendation engine driving engagement
- Amazon: Supply chain optimization and personalization
- JPMorgan: AI for contract analysis and trading
- Stitch Fix: AI-powered personal styling
- Alibaba: Intelligent customer service and logistics
    """
}

# Real assessment questions with proper answers
REAL_ASSESSMENT_QUESTIONS = [
    {
        'text': 'What distinguishes Machine Learning from traditional programming?',
        'options': [
            ('Machine Learning learns from data without explicit programming', True),
            ('Machine Learning requires more code than traditional programming', False),
            ('Machine Learning only works with numerical data', False),
            ('Machine Learning cannot handle complex problems', False),
        ],
        'explanation': 'Machine Learning enables systems to learn and improve from experience automatically, without being explicitly programmed for every scenario.'
    },
    {
        'text': 'Which of the following is NOT a type of Machine Learning?',
        'options': [
            ('Supervised Learning', False),
            ('Unsupervised Learning', False),
            ('Reinforcement Learning', False),
            ('Deterministic Learning', True),
        ],
        'explanation': 'The three main types of Machine Learning are Supervised, Unsupervised, and Reinforcement Learning. Deterministic Learning is not a recognized ML type.'
    },
    {
        'text': 'What is the primary purpose of training data in Machine Learning?',
        'options': [
            ('To teach the model patterns and relationships', True),
            ('To test the final model performance', False),
            ('To validate hyperparameters', False),
            ('To visualize data distribution', False),
        ],
        'explanation': 'Training data is used to teach the ML model to recognize patterns and relationships that it can then apply to new, unseen data.'
    },
    {
        'text': 'In AI ethics, what does "algorithmic bias" refer to?',
        'options': [
            ('Systematic errors that create unfair outcomes for certain groups', True),
            ('Technical bugs in the code', False),
            ('Preference for certain programming languages', False),
            ('Speed differences in algorithm execution', False),
        ],
        'explanation': 'Algorithmic bias refers to systematic and repeatable errors in AI systems that create unfair outcomes, often disadvantaging certain demographic groups.'
    },
    {
        'text': 'What is Deep Learning?',
        'options': [
            ('A subset of ML using neural networks with multiple layers', True),
            ('Learning from very large datasets only', False),
            ('A technique for database management', False),
            ('A method for compressing data', False),
        ],
        'explanation': 'Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers (deep networks) to progressively extract higher-level features from raw input.'
    },
    {
        'text': 'What is the main advantage of Convolutional Neural Networks (CNNs) for image processing?',
        'options': [
            ('They can automatically learn spatial hierarchies of features', True),
            ('They require less training data than other methods', False),
            ('They work only with black and white images', False),
            ('They eliminate the need for GPUs', False),
        ],
        'explanation': 'CNNs use convolutional layers to automatically learn spatial hierarchies of features, making them highly effective for image-related tasks.'
    },
    {
        'text': 'In Natural Language Processing, what is tokenization?',
        'options': [
            ('Breaking text into smaller units like words or subwords', True),
            ('Encrypting text for security', False),
            ('Translating text to another language', False),
            ('Removing punctuation from text', False),
        ],
        'explanation': 'Tokenization is the process of breaking down text into smaller units (tokens) such as words, subwords, or characters, which is a fundamental step in NLP.'
    },
    {
        'text': 'Which of the following best describes "overfitting" in Machine Learning?',
        'options': [
            ('Model performs well on training data but poorly on new data', True),
            ('Model takes too long to train', False),
            ('Model uses too much memory', False),
            ('Model cannot learn from the training data', False),
        ],
        'explanation': 'Overfitting occurs when a model learns the training data too well, including noise and outliers, resulting in poor generalization to new, unseen data.'
    },
    {
        'text': 'What is the primary goal of Reinforcement Learning?',
        'options': [
            ('Learning optimal actions through trial and error with rewards', True),
            ('Classifying data into predefined categories', False),
            ('Finding patterns in unlabeled data', False),
            ('Compressing data for storage', False),
        ],
        'explanation': 'Reinforcement Learning involves an agent learning to make optimal decisions by interacting with an environment and receiving rewards or penalties.'
    },
    {
        'text': 'Which ethical principle requires AI systems to provide understandable reasons for their decisions?',
        'options': [
            ('Transparency and Explainability', True),
            ('Privacy Protection', False),
            ('Fairness', False),
            ('Accountability', False),
        ],
        'explanation': 'Transparency and explainability require that AI systems provide clear, understandable explanations for their decisions, especially in high-stakes applications.'
    },
    {
        'text': 'What is transfer learning in the context of Deep Learning?',
        'options': [
            ('Using knowledge from one task to improve learning on another task', True),
            ('Transferring data between different databases', False),
            ('Moving models from one computer to another', False),
            ('Converting models to different programming languages', False),
        ],
        'explanation': 'Transfer learning involves using a model trained on one task and adapting it for a related task, often significantly reducing training time and data requirements.'
    },
    {
        'text': 'In healthcare AI, what is a major concern regarding patient data?',
        'options': [
            ('Privacy and confidentiality of sensitive medical information', True),
            ('Storage space requirements', False),
            ('Color formatting of medical records', False),
            ('Font size in digital records', False),
        ],
        'explanation': 'Patient data privacy and confidentiality are critical concerns in healthcare AI, as medical records contain highly sensitive personal information.'
    },
    {
        'text': 'What is the purpose of a validation dataset in Machine Learning?',
        'options': [
            ('To tune hyperparameters and prevent overfitting', True),
            ('To train the final model', False),
            ('To deploy the model in production', False),
            ('To collect more training data', False),
        ],
        'explanation': 'The validation dataset is used during training to tune hyperparameters and evaluate model performance, helping to prevent overfitting.'
    },
    {
        'text': 'Which of the following is an example of AI bias in real-world applications?',
        'options': [
            ('Facial recognition systems performing poorly on certain demographics', True),
            ('AI systems requiring electricity to operate', False),
            ('Machine learning models needing training data', False),
            ('Neural networks having multiple layers', False),
        ],
        'explanation': 'Facial recognition systems have shown bias by performing less accurately on certain demographic groups, often due to imbalanced training data.'
    },
    {
        'text': 'What does GDPR primarily regulate in the context of AI?',
        'options': [
            ('Personal data protection and privacy', True),
            ('Algorithm efficiency', False),
            ('Model accuracy requirements', False),
            ('Programming language standards', False),
        ],
        'explanation': 'The General Data Protection Regulation (GDPR) is a European regulation that primarily governs how personal data is collected, processed, and protected.'
    }
]


class Command(BaseCommand):
    help = 'Populate database with realistic data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting comprehensive data population...')
        
        # Create users
        self.create_users()
        
        # Create AI Literacy content
        self.create_frameworks()
        self.create_modules()
        self.create_student_progress()
        
        # Create assessments
        self.create_assessments()
        self.create_questions()
        self.create_assessment_attempts()
        
        # Create curriculum
        self.create_curriculum()
        self.create_assignments()
        self.create_submissions()
        
        # Create inclusivity programs
        self.create_interventions()
        self.create_mentorship()
        self.create_resources()
        
        # Create ethics content
        self.create_ethical_principles()
        self.create_case_studies()
        self.create_forums()
        
        self.stdout.write(self.style.SUCCESS('✅ Data population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📚 Total Modules: {LearningModule.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📝 Total Assessments: {AssessmentAttempt.objects.count()}'))

    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Create admin users
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@ailiteracy.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                role='admin',
                institution='AI Literacy Platform',
                is_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user: {admin.username}'))
        
        # Create faculty
        disciplines = ['Computer Science', 'Engineering', 'Business', 'Medicine', 'Arts', 'Sciences']
        institutions = ['IIT Delhi', 'IIT Bombay', 'BITS Pilani', 'NIT Trichy', 'Anna University']
        
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'faculty{i+1}',
                defaults={
                    'email': f'faculty{i+1}@university.edu',
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'role': 'faculty',
                    'discipline': random.choice(disciplines),
                    'institution': random.choice(institutions),
                    'gender': random.choice(['male', 'female']),
                    'country': 'India',
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('faculty123')
                user.save()
                self.stdout.write(f'✓ Created faculty: {user.username}')
        
        # Create students (100 students for statistical significance)
        genders = ['male', 'female', 'male', 'female', 'other']  # Balanced distribution
        
        for i in range(100):
            user, created = User.objects.get_or_create(
                username=f'student{i+1}',
                defaults={
                    'email': f'student{i+1}@university.edu',
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'role': 'student',
                    'discipline': random.choice(disciplines),
                    'institution': random.choice(institutions),
                    'gender': random.choice(genders),
                    'country': 'India',
                    'enrollment_year': random.randint(2020, 2026),
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('student123')
                user.save()
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {User.objects.count()} total users'))

    def create_frameworks(self):
        self.stdout.write('Creating AI Literacy Frameworks...')
        
        faculty = User.objects.filter(role='faculty').first()
        
        frameworks_data = [
            {
                'title': 'Introduction to Artificial Intelligence',
                'description': 'Foundational concepts in AI including machine learning, neural networks, and AI applications across industries',
                'discipline': 'Computer Science',
                'difficulty_level': 'beginner',
            },
            {
                'title': 'AI in Healthcare',
                'description': 'Applications of AI in medical diagnosis, treatment planning, drug discovery, and healthcare management',
                'discipline': 'Medicine',
                'difficulty_level': 'intermediate',
            },
            {
                'title': 'Business Intelligence and AI',
                'description': 'Using AI for business analytics, customer insights, decision making, and predictive modeling',
                'discipline': 'Business',
                'difficulty_level': 'intermediate',
            },
            {
                'title': 'AI Ethics and Responsible AI',
                'description': 'Ethical implications of AI, algorithmic bias, fairness, transparency, and societal impact',
                'discipline': '',
                'difficulty_level': 'beginner',
            },
            {
                'title': 'Advanced Machine Learning',
                'description': 'Deep learning, reinforcement learning, neural architectures, and advanced ML algorithms',
                'discipline': 'Computer Science',
                'difficulty_level': 'advanced',
            },
        ]
        
        for data in frameworks_data:
            framework, created = AILiteracyFramework.objects.get_or_create(
                title=data['title'],
                defaults={**data, 'created_by': faculty, 'is_active': True}
            )
            if created:
                self.stdout.write(f'✓ Created framework: {framework.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total frameworks: {AILiteracyFramework.objects.count()}'))

    def create_modules(self):
        self.stdout.write('Creating learning modules with real content...')
        
        frameworks = AILiteracyFramework.objects.all()
        
        for framework in frameworks:
            module_count = 0
            # Use real content from AI_MODULES_CONTENT
            for topic, content in AI_MODULES_CONTENT.items():
                if module_count >= 6:  # Limit modules per framework
                    break
                
                # Extract first paragraph as description
                description = content.split('\n\n')[0] if '\n\n' in content else content[:200]
                
                module, created = LearningModule.objects.get_or_create(
                    framework=framework,
                    title=topic,
                    defaults={
                        'description': description,
                        'content': content,
                        'order': module_count + 1,
                        'duration_minutes': random.choice([30, 45, 60, 90]),
                        'is_published': True,
                    }
                )
                if created:
                    module_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {LearningModule.objects.count()} modules with real content'))

    def create_student_progress(self):
        self.stdout.write('Creating student progress records...')
        
        students = User.objects.filter(role='student')
        modules = LearningModule.objects.filter(is_published=True)
        
        progress_count = 0
        for student in students:
            # Each student starts 3-10 modules
            selected_modules = random.sample(list(modules), random.randint(3, min(10, len(modules))))
            
            for module in selected_modules:
                completed = random.choice([True, True, False])  # 66% completion rate
                
                progress, created = StudentProgress.objects.get_or_create(
                    student=student,
                    module=module,
                    defaults={
                        'progress_percentage': 100 if completed else random.randint(20, 80),
                        'time_spent_minutes': random.randint(20, module.duration_minutes + 30),
                        'started_at': timezone.now() - timedelta(days=random.randint(1, 60)),
                    }
                )
                
                if created and completed:
                    progress.completed_at = progress.started_at + timedelta(days=random.randint(1, 14))
                    progress.save()
                    progress_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {StudentProgress.objects.count()} progress records'))

    def create_assessments(self):
        self.stdout.write('Creating assessments...')
        
        faculty = User.objects.filter(role='faculty').first()
        
        assessments_data = [
            {
                'title': 'AI Fundamentals Assessment',
                'description': 'Comprehensive test covering basic AI concepts, machine learning, and neural networks',
                'category': 'technical',
                'discipline_specific': 'Computer Science',
            },
            {
                'title': 'AI Conceptual Understanding',
                'description': 'Evaluate conceptual knowledge of AI principles, history, and applications',
                'category': 'conceptual',
                'discipline_specific': '',
            },
            {
                'title': 'AI Application Skills Test',
                'description': 'Practical assessment of ability to apply AI concepts to real-world scenarios',
                'category': 'application',
                'discipline_specific': '',
            },
            {
                'title': 'AI Ethics Awareness Quiz',
                'description': 'Assessment of understanding ethical considerations, bias, fairness, and responsible AI',
                'category': 'ethical',
                'discipline_specific': '',
            },
        ]
        
        for data in assessments_data:
            questionnaire, created = ReadinessQuestionnaire.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'created_by': faculty,
                    'time_limit_minutes': 45,
                    'passing_score': 60,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'✓ Created assessment: {questionnaire.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total assessments: {ReadinessQuestionnaire.objects.count()}'))

    def create_questions(self):
        self.stdout.write('Creating assessment questions with real content...')
        
        questionnaires = ReadinessQuestionnaire.objects.all()
        
        for questionnaire in questionnaires:
            # Clear existing questions
            questionnaire.questions.all().delete()
            
            # Add all real questions to each questionnaire
            for i, q_data in enumerate(REAL_ASSESSMENT_QUESTIONS):
                question = Question.objects.create(
                    questionnaire=questionnaire,
                    question_text=q_data['text'],
                    question_type='mcq',
                    order=i + 1,
                    points=10,
                    explanation=q_data['explanation']
                )
                
                for j, (option_text, is_correct) in enumerate(q_data['options']):
                    QuestionOption.objects.create(
                        question=question,
                        option_text=option_text,
                        is_correct=is_correct,
                        order=j + 1,
                    )
            
            questionnaire.total_questions = questionnaire.questions.count()
            questionnaire.save()
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {Question.objects.count()} real questions'))

    def create_assessment_attempts(self):
        self.stdout.write('Creating assessment attempts...')
        
        students = User.objects.filter(role='student')
        questionnaires = ReadinessQuestionnaire.objects.all()
        
        attempt_count = 0
        for student in students:
            # Each student attempts 1-3 assessments
            for questionnaire in random.sample(list(questionnaires), random.randint(1, min(3, len(questionnaires)))):
                questions = questionnaire.questions.all()
                total_points = sum(q.points for q in questions)
                
                # Simulate varying performance
                base_score = random.uniform(40, 95)
                if questionnaire.discipline_specific and questionnaire.discipline_specific == student.discipline:
                    base_score = random.uniform(60, 95)
                
                attempt = AssessmentAttempt.objects.create(
                    student=student,
                    questionnaire=questionnaire,
                    started_at=timezone.now() - timedelta(days=random.randint(1, 45)),
                    total_points=total_points,
                )
                
                earned_points = 0
                for question in questions:
                    options = list(question.options.all())
                    correct_option = next((opt for opt in options if opt.is_correct), None)
                    
                    # Simulate answer based on performance
                    if random.uniform(0, 100) < base_score:
                        selected_option = correct_option
                        is_correct = True
                        points = question.points
                    else:
                        wrong_options = [opt for opt in options if not opt.is_correct]
                        selected_option = random.choice(wrong_options) if wrong_options else options[0]
                        is_correct = False
                        points = 0
                    
                    earned_points += points
                    
                    StudentResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option=selected_option,
                        is_correct=is_correct,
                        points_earned=points,
                    )
                
                attempt.completed_at = attempt.started_at + timedelta(minutes=random.randint(20, 45))
                attempt.score = (earned_points / total_points * 100) if total_points > 0 else 0
                attempt.passed = attempt.score >= questionnaire.passing_score
                attempt.save()
                attempt_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {attempt_count} assessment attempts'))

    def create_curriculum(self):
        self.stdout.write('Creating curriculum integrations...')
        
        faculty = User.objects.filter(role='faculty')
        disciplines = ['Computer Science', 'Engineering', 'Business', 'Medicine']
        
        for i, discipline in enumerate(disciplines):
            faculty_member = random.choice(faculty)
            curriculum, created = CurriculumIntegration.objects.get_or_create(
                title=f"AI Integration in {discipline}",
                defaults={
                    'discipline': discipline,
                    'course_code': f'AI{1000 + i}',
                    'semester': random.randint(1, 8),
                    'description': f'Comprehensive integration of AI concepts into {discipline} curriculum',
                    'learning_objectives': f'Students will understand AI applications in {discipline}, develop practical skills, and apply AI techniques to domain-specific problems.',
                    'created_by': faculty_member,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'✓ Created curriculum: {curriculum.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total curriculum integrations: {CurriculumIntegration.objects.count()}'))

    def create_assignments(self):
        self.stdout.write('Creating assignments...')
        
        curriculums = CurriculumIntegration.objects.all()
        assignment_types = ['case_study', 'project', 'presentation', 'research', 'practical']
        
        for curriculum in curriculums:
            for i in range(random.randint(2, 4)):
                Assignment.objects.create(
                    curriculum=curriculum,
                    title=f"{curriculum.discipline} AI Project {i+1}",
                    description=f"Apply AI techniques to solve real-world problems in {curriculum.discipline}",
                    assignment_type=random.choice(assignment_types),
                    instructions=f"Complete the {curriculum.discipline}-specific AI task following the provided guidelines. Submit your work and a reflection on the learning outcomes.",
                    due_date=timezone.now() + timedelta(days=random.randint(7, 60)),
                    max_points=100,
                )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {Assignment.objects.count()} assignments'))

    def create_submissions(self):
        self.stdout.write('Creating assignment submissions...')
        
        students = User.objects.filter(role='student')
        assignments = Assignment.objects.all()
        faculty = list(User.objects.filter(role='faculty'))
        
        submission_count = 0
        for student in students:
            for assignment in random.sample(list(assignments), random.randint(1, min(3, len(assignments)))):
                submission = AssignmentSubmission.objects.create(
                    assignment=assignment,
                    student=student,
                    submission_text=f"Completed {assignment.title}. Analysis and implementation attached.",
                    submitted_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                )
                
                # 70% graded
                if random.random() < 0.7:
                    submission.grade = random.uniform(50, 100)
                    submission.feedback = f"Good work on {assignment.title}. {'Excellent analysis.' if submission.grade > 80 else 'Consider improving your approach.'}"
                    submission.graded_by = random.choice(faculty)
                    submission.graded_at = submission.submitted_at + timedelta(days=random.randint(1, 7))
                    submission.save()
                
                submission_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {submission_count} submissions'))

    def create_interventions(self):
        self.stdout.write('Creating intervention programs...')
        
        faculty = list(User.objects.filter(role='faculty'))
        
        interventions_data = [
            {
                'title': 'Women in AI Initiative',
                'target_group': 'gender_gap',
                'description': 'Program to encourage and support women in AI education through mentorship and resources',
                'objectives': 'Increase female participation in AI, provide role models, create supportive community',
            },
            {
                'title': 'Cross-Disciplinary AI Skills',
                'target_group': 'discipline_gap',
                'description': 'Bridge AI knowledge gaps across different academic disciplines',
                'objectives': 'Enable all students to understand and apply AI regardless of their major',
            },
            {
                'title': 'AI for All Cultures',
                'target_group': 'cultural_gap',
                'description': 'Ensure AI education is accessible and relevant across diverse cultural backgrounds',
                'objectives': 'Promote inclusive AI development and reduce cultural bias in AI systems',
            },
        ]
        
        for data in interventions_data:
            intervention, created = InterventionProgram.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'start_date': timezone.now().date(),
                    'end_date': (timezone.now() + timedelta(days=180)).date(),
                    'coordinator': random.choice(faculty),
                    'max_participants': 50,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'✓ Created intervention: {intervention.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total interventions: {InterventionProgram.objects.count()}'))

    def create_mentorship(self):
        self.stdout.write('Creating mentorship programs...')
        
        faculty = User.objects.filter(role='faculty')
        students = list(User.objects.filter(role='student'))
        
        for mentor in faculty:
            program = MentorshipProgram.objects.create(
                title=f"AI Mentorship with {mentor.get_full_name()}",
                description=f"One-on-one mentorship in {mentor.discipline} and AI applications",
                discipline=mentor.discipline,
                mentor=mentor,
                max_mentees=5,
                is_accepting=True,
            )
            
            # Enroll 2-4 students
            for student in random.sample(students, random.randint(2, 4)):
                MentorshipEnrollment.objects.create(
                    program=program,
                    mentee=student,
                    status='active',
                )
                program.current_mentees += 1
            
            program.save()
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {MentorshipProgram.objects.count()} mentorship programs'))

    def create_resources(self):
        self.stdout.write('Creating support resources...')
        
        faculty = list(User.objects.filter(role='faculty'))
        
        resources_data = [
            ('AI Learning Roadmap', 'guide', 'Comprehensive guide to learning AI from beginner to advanced'),
            ('Python for AI - Tutorial', 'tutorial', 'Step-by-step Python programming tutorial for AI applications'),
            ('Machine Learning Basics Video', 'video', 'Video series covering machine learning fundamentals'),
            ('AI Ethics Guidelines', 'document', 'Guidelines for ethical AI development and deployment'),
            ('TensorFlow Practice Exercises', 'tool', 'Hands-on exercises for TensorFlow deep learning framework'),
        ]
        
        for title, resource_type, description in resources_data:
            resource, created = SupportResource.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'resource_type': resource_type,
                    'target_audience': 'All students',
                    'created_by': random.choice(faculty),
                }
            )
            if created:
                self.stdout.write(f'✓ Created resource: {resource.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total resources: {SupportResource.objects.count()}'))

    def create_ethical_principles(self):
        self.stdout.write('Creating ethical principles...')
        
        faculty = list(User.objects.filter(role='faculty'))
        
        principles_data = [
            {
                'title': 'Fairness and Bias Mitigation',
                'category': 'fairness',
                'description': 'AI systems should be designed to minimize bias and ensure fair treatment across all user groups',
                'examples': 'Ensuring hiring algorithms do not discriminate based on gender or ethnicity. Testing facial recognition across diverse demographics.',
                'resources': 'Research papers on algorithmic fairness, bias detection tools, fairness metrics documentation',
            },
            {
                'title': 'Transparency and Explainability',
                'category': 'transparency',
                'description': 'AI decision-making processes should be explainable and understandable to stakeholders',
                'examples': 'Providing clear explanations for loan approval decisions. Using interpretable models in medical diagnosis.',
                'resources': 'LIME and SHAP explainability libraries, EU AI Act transparency requirements',
            },
            {
                'title': 'Privacy and Data Protection',
                'category': 'privacy',
                'description': 'User data must be handled securely and privacy must be respected throughout AI development',
                'examples': 'Implementing encryption in AI healthcare applications. Using differential privacy in data analysis.',
                'resources': 'GDPR compliance guidelines, privacy-preserving machine learning techniques',
            },
        ]
        
        for data in principles_data:
            principle, created = EthicalPrinciple.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'created_by': random.choice(faculty),
                }
            )
            if created:
                self.stdout.write(f'✓ Created principle: {principle.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total ethical principles: {EthicalPrinciple.objects.count()}'))

    def create_case_studies(self):
        self.stdout.write('Creating ethical case studies...')
        
        faculty = list(User.objects.filter(role='faculty'))
        
        case_studies_data = [
            {
                'title': 'Facial Recognition and Privacy',
                'scenario': 'A city government wants to implement facial recognition technology in public spaces for security purposes. The system would identify individuals in real-time and flag those on watchlists. Consider the privacy implications, potential for misuse, accuracy concerns across demographics, and balance with public safety.',
                'discipline': 'Computer Science',
                'difficulty_level': 'intermediate',
                'learning_objectives': 'Understand privacy vs security tradeoffs, recognize bias in facial recognition, evaluate ethical implications of surveillance',
                'discussion_questions': 'What are the potential benefits and harms? How can bias be addressed? What regulations should govern such systems? Who should have access to the data?',
            },
            {
                'title': 'AI in Medical Diagnosis',
                'scenario': 'An AI system has been developed to provide medical diagnoses based on patient symptoms and test results. The system achieves 95% accuracy but occasionally makes errors. A patient receives an incorrect diagnosis from the AI. Who is responsible - the AI developer, the hospital, or the doctor who relied on the AI?',
                'discipline': 'Medicine',
                'difficulty_level': 'advanced',
                'learning_objectives': 'Analyze accountability in AI systems, understand human-AI collaboration in healthcare, evaluate risk management',
                'discussion_questions': 'How should liability be distributed? What role should humans play in AI-assisted diagnosis? How can we ensure patient safety while leveraging AI benefits?',
            },
        ]
        
        for data in case_studies_data:
            case_study, created = EthicalCaseStudy.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'description': data['scenario'][:200],
                    'created_by': random.choice(faculty),
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(f'✓ Created case study: {case_study.title}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Total case studies: {EthicalCaseStudy.objects.count()}'))

    def create_forums(self):
        self.stdout.write('Creating discussion forums...')
        
        users = list(User.objects.all())
        case_studies = EthicalCaseStudy.objects.all()
        
        for case_study in case_studies:
            forum = DiscussionForum.objects.create(
                case_study=case_study,
                title=f"Discussion: {case_study.title}",
                description=f"Discuss ethical implications and perspectives on {case_study.title}",
                created_by=random.choice(users),
                is_active=True,
            )
            
            # Create discussion posts
            for _ in range(random.randint(3, 5)):
                DiscussionPost.objects.create(
                    forum=forum,
                    author=random.choice(users),
                    content=fake.paragraph(nb_sentences=random.randint(3, 6)),
                )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {DiscussionForum.objects.count()} forums with discussions'))
