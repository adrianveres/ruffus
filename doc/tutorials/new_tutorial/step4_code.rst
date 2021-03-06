.. include:: ../../global.inc
.. _New_Tutorial_4th_step_code:


######################################################################################################################################
New Tutorial in revision Code for Step 4: Understanding how your pipeline works
######################################################################################################################################

* :ref:`New tutorial overview <New_Tutorial>`
* :ref:`pipeline functions <pipeline_functions>` in detail
* :ref:`Back to Step 4 <New_Tutorial_4th_step>`

******************************************
Display the initial state of the pipeline
******************************************
    ::

        from ruffus import *
        import sys

        #---------------------------------------------------------------
        #   create initial files
        #
        @originate([   ['job1.a.start', 'job1.b.start'],
                       ['job2.a.start', 'job2.b.start'],
                       ['job3.a.start', 'job3.b.start']    ])
        def create_initial_file_pairs(output_files):
            # create both files as necessary
            for output_file in output_files:
                with open(output_file, "w") as oo: pass

        #---------------------------------------------------------------
        #   first task
        @transform(create_initial_file_pairs, suffix(".start"), ".output.1")
        def first_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #   second task
        @transform(first_task, suffix(".output.1"), ".output.2")
        def second_task(input_files, output_file):
            with open(output_file, "w"): pass

        pipeline_printout(sys.stdout, [second_task])
        pipeline_printout(sys.stdout, [second_task], verbose = 3)

************************************
Normal Output
************************************
    ::

        >>> pipeline_printout(sys.stdout, [second_task])

        ________________________________________
        Tasks which will be run:

        Task = create_initial_file_pairs
        Task = first_task
        Task = second_task


************************************
High Verbosity Output
************************************

    ::

        >>> pipeline_printout(sys.stdout, [second_task], verbose = 3)

        ________________________________________
        Tasks which will be run:

        Task = create_initial_file_pairs
               Job  = [None
                     -> job1.a.start
                     -> job1.b.start]
                 Job needs update: Missing files [job1.a.start, job1.b.start]
               Job  = [None
                     -> job2.a.start
                     -> job2.b.start]
                 Job needs update: Missing files [job2.a.start, job2.b.start]
               Job  = [None
                     -> job3.a.start
                     -> job3.b.start]
                 Job needs update: Missing files [job3.a.start, job3.b.start]

        Task = first_task
               Job  = [[job1.a.start, job1.b.start]
                     -> job1.a.output.1]
                 Job needs update: Missing files [job1.a.start, job1.b.start, job1.a.output.1]
               Job  = [[job2.a.start, job2.b.start]
                     -> job2.a.output.1]
                 Job needs update: Missing files [job2.a.start, job2.b.start, job2.a.output.1]
               Job  = [[job3.a.start, job3.b.start]
                     -> job3.a.output.1]
                 Job needs update: Missing files [job3.a.start, job3.b.start, job3.a.output.1]

        Task = second_task
               Job  = [job1.a.output.1
                     -> job1.a.output.2]
                 Job needs update: Missing files [job1.a.output.1, job1.a.output.2]
               Job  = [job2.a.output.1
                     -> job2.a.output.2]
                 Job needs update: Missing files [job2.a.output.1, job2.a.output.2]
               Job  = [job3.a.output.1
                     -> job3.a.output.2]
                 Job needs update: Missing files [job3.a.output.1, job3.a.output.2]

        ________________________________________

******************************************
Display the partially up-to-date pipeline
******************************************
    Run the pipeline, modify ``job1.stage`` so that the second task is no longer up-to-date
    and printout the pipeline stage again::

        >>> pipeline_run([second_task])
            Job  = [None -> [job1.a.start, job1.b.start]] completed
            Job  = [None -> [job2.a.start, job2.b.start]] completed
            Job  = [None -> [job3.a.start, job3.b.start]] completed
        Completed Task = create_initial_file_pairs
            Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] completed
            Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] completed
            Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] completed
        Completed Task = first_task
            Job  = [job1.a.output.1 -> job1.a.output.2] completed
            Job  = [job2.a.output.1 -> job2.a.output.2] completed
            Job  = [job3.a.output.1 -> job3.a.output.2] completed
        Completed Task = second_task


        # modify job1.stage1
        >>> open("job1.a.output.1", "w").close()

    At a verbosity of 5, even jobs which are up-to-date will be displayed::

        >>> pipeline_printout(sys.stdout, [second_task], verbose = 5)
        ________________________________________
        Tasks which are up-to-date:

        Task = create_initial_file_pairs
               Job  = [None
                     -> job1.a.start
                     -> job1.b.start]
                 Job up-to-date
               Job  = [None
                     -> job2.a.start
                     -> job2.b.start]
                 Job up-to-date
               Job  = [None
                     -> job3.a.start
                     -> job3.b.start]
                 Job up-to-date

        Task = first_task
               Job  = [[job1.a.start, job1.b.start]
                     -> job1.a.output.1]
                 Job up-to-date
               Job  = [[job2.a.start, job2.b.start]
                     -> job2.a.output.1]
                 Job up-to-date
               Job  = [[job3.a.start, job3.b.start]
                     -> job3.a.output.1]
                 Job up-to-date


        ________________________________________
        Tasks which will be run:

        Task = second_task
               Job  = [job1.a.output.1
                     -> job1.a.output.2]
                 Job needs update:
                 Input files:
                  * 05 Dec 2013 12:04:52.80: job1.a.output.1
                 Output files:
                  * 05 Dec 2013 12:01:29.01: job1.a.output.2

               Job  = [job2.a.output.1
                     -> job2.a.output.2]
                 Job up-to-date
               Job  = [job3.a.output.1
                     -> job3.a.output.2]
                 Job up-to-date

        ________________________________________


    We can now see that the there is only one job in "second_task" which needs to be re-run
    because 'job1.stage1' has been modified after 'job1.stage2'
