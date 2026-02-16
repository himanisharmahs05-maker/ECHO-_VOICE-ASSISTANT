

                    except sr.UnknownValueError:
                        speak("Sorry, I didn't understand. Say it again.")
                    except sr.RequestError:
                        speak("Internet issue, I can't process speech right now.")

        except Exception as e:
            print("Error:", e)
            speak("Something went wrong but I'm still running.")