'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Home, Sparkles, ArrowRight } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-crimson-50/30 to-white">
      <nav className="border-b border-crimson-100 bg-white/95 backdrop-blur-md sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Home className="h-6 w-6 text-crimson-600" />
              <span className="font-bold text-xl text-crimson-700">UMass Housing</span>
            </div>
            <div className="hidden md:flex space-x-8">
              <Link href="/" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                Home
              </Link>
              <Link href="/recommender" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                Recommender
              </Link>
              <Link href="/about" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                About
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main>
        <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
          <div
            className="absolute inset-0 opacity-5"
            style={{
              backgroundImage: 'url(https://images.pexels.com/photos/1370704/pexels-photo-1370704.jpeg)',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }}
          />

          <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-crimson-50 rounded-full mb-6 border border-crimson-100">
            <Sparkles className="h-4 w-4 text-crimson-600" />
            <span className="text-sm font-medium text-crimson-700">Smart Housing Recommendations</span>
          </div>

            <h1 className="text-5xl md:text-6xl font-extrabold mb-6 tracking-tight">
              <span className="text-3d-large text-crimson-700">Find Your Perfect</span>
              <br />
              <span className="text-3d text-crimson-600">UMass Home</span>
            </h1>

            <p className="text-xl text-gray-700 mb-10 max-w-2xl mx-auto font-normal leading-relaxed">
              Answer a few questions about your lifestyle and preferences, and we'll match you
              with the residence halls that best fit your needs.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/recommender">
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-crimson-600 to-crimson-700 hover:from-crimson-700 hover:to-crimson-800 text-white px-8 py-6 text-lg rounded-xl shadow-lg hover:shadow-xl transition-all font-semibold"
                >
                  Start Recommender
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-crimson-200 text-crimson-700 hover:bg-crimson-50 hover:border-crimson-300 px-8 py-6 text-lg rounded-xl transition-all font-semibold bg-white"
                >
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-crimson-700 mb-16 tracking-tight">
              How It Works
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-white to-crimson-50/50 hover:shadow-xl transition-all duration-300 border border-crimson-100 hover:border-crimson-200 hover:-translate-y-1">
                <div className="w-16 h-16 bg-gradient-to-br from-crimson-600 to-crimson-700 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <span className="text-2xl font-bold text-white">1</span>
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-900">Answer Questions</h3>
                <p className="text-gray-600 leading-relaxed">
                  Complete our comprehensive questionnaire about your preferences, lifestyle, and needs.
                </p>
              </div>

              <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-white to-crimson-50/50 hover:shadow-xl transition-all duration-300 border border-crimson-100 hover:border-crimson-200 hover:-translate-y-1">
                <div className="w-16 h-16 bg-gradient-to-br from-crimson-600 to-crimson-700 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <span className="text-2xl font-bold text-white">2</span>
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-900">Get Matched</h3>
                <p className="text-gray-600 leading-relaxed">
                  Our algorithm analyzes your responses and matches you with compatible residence halls.
                </p>
              </div>

              <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-white to-crimson-50/50 hover:shadow-xl transition-all duration-300 border border-crimson-100 hover:border-crimson-200 hover:-translate-y-1">
                <div className="w-16 h-16 bg-gradient-to-br from-crimson-600 to-crimson-700 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <span className="text-2xl font-bold text-white">3</span>
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-900">Choose Wisely</h3>
                <p className="text-gray-600 leading-relaxed">
                  Review your top matches with detailed information to make an informed decision.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-crimson-600 via-crimson-650 to-crimson-700 relative overflow-hidden">
          <div className="absolute inset-0 bg-black/5"></div>
          <div className="max-w-4xl mx-auto text-center relative z-10">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6 tracking-tight">
              Ready to Find Your Perfect Dorm?
            </h2>
            <p className="text-lg text-crimson-50 mb-10 font-normal">
              Join hundreds of students who have found their ideal residence hall match.
            </p>
            <Link href="/recommender">
              <Button
                size="lg"
                className="bg-white hover:bg-crimson-50 text-crimson-700 px-8 py-6 text-lg rounded-xl shadow-xl hover:shadow-2xl transition-all font-semibold"
              >
                Get Started Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="bg-gradient-to-r from-crimson-900 to-crimson-800 text-white py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-crimson-100">
            Unofficial student project — © {new Date().getFullYear()} UMass Amherst Smart Housing Recommender
          </p>
          <p className="text-sm text-crimson-200 mt-2">
            Not affiliated with the University of Massachusetts Amherst
          </p>
        </div>
      </footer>
    </div>
  );
}
